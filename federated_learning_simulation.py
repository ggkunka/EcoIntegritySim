import flwr as fl
import tensorflow as tf
from tensorflow import keras
import numpy as np
from web3 import Web3
import json
import pandas as pd
import multiprocessing
import time
import argparse

# Path to the ABI file
ABI_PATH = '/Users/jayaprakash/EcoIntegritySim/eco-integrity-contract/build/contracts/EcoIntegrity.json'

# Argument parsing for contract address and network ID
parser = argparse.ArgumentParser()
parser.add_argument("--contract_address", required=True, help="Contract address deployed by Truffle")
parser.add_argument("--network_id", required=True, help="Network ID on which the contract was deployed")
args = parser.parse_args()

# Connect to Ganache blockchain
ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
assert web3.is_connected(), "Ganache connection failed"

# Load contract ABI and address from the JSON file
def load_contract_abi(abi_path, network_id):
    with open(abi_path) as f:
        contract_json = json.load(f)
        contract_abi = contract_json['abi']
        if network_id in contract_json['networks']:
            contract_address = contract_json['networks'][network_id]['address']
        else:
            raise KeyError(f"Network ID {network_id} not found in ABI file.")
    return contract_abi, contract_address

# Load the contract ABI and address
try:
    contract_abi, contract_address = load_contract_abi(ABI_PATH, args.network_id)
    print(f"Contract ABI loaded successfully. Contract address: {contract_address}")
except KeyError as e:
    print(f"Error loading contract: {str(e)}")
    exit(1)

# Load the contract using Web3
eco_integrity = web3.eth.contract(address=contract_address, abi=contract_abi)

# Define a neural network model
def build_model(input_dim):
    model = keras.Sequential([
        keras.layers.InputLayer(input_shape=(input_dim,)),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Load ToNIoT dataset without unnecessary row dropping
def load_toniot_weather_data(file_path):
    data = pd.read_csv(file_path)
    
    # Strip any extra spaces (just in case)
    data['date'] = data['date'].str.strip()
    data['time'] = data['time'].str.strip()

    # Parse the timestamp without dropping any rows
    data['timestamp'] = pd.to_datetime(data['date'] + ' ' + data['time'], format='%d-%b-%y %H:%M:%S')

    # Select relevant features: temperature, pressure, humidity, label
    X = data[['temperature', 'pressure', 'humidity']].values
    y = data['label'].values  # Label indicates attack (1) or benign (0)

    return X, y

# Load and preprocess data
X, y = load_toniot_weather_data('Train_Test_IoT_Weather.csv')

# Split the dataset into training and test sets
X_train, X_test = X[:800], X[800:]
y_train, y_test = y[:800], y[800:]

# Flower client for Federated Learning
class FLClient(fl.client.NumPyClient):
    def __init__(self, model):
        self.model = model

    def get_parameters(self, config):
        print("Client: Sending initial parameters to the server...")
        return self.model.get_weights()

    def fit(self, parameters, config):
        print("Client: Training model with provided parameters...")
        self.model.set_weights(parameters)
        self.model.fit(X_train, y_train, epochs=1, verbose=0)

        # Log model update hash to blockchain
        model_hash = "hash_of_model_update"
        tx_hash = eco_integrity.functions.logData(model_hash).transact({'from': web3.eth.accounts[0]})
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Model update {model_hash} logged successfully in blockchain")

        return self.model.get_weights(), len(X_train), {}

    def evaluate(self, parameters, config):
        print("Client: Evaluating model...")
        self.model.set_weights(parameters)
        loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
        
        print(f"Client: Evaluation - Loss: {loss}, Accuracy: {accuracy}")
        return loss, len(X_test), {"accuracy": accuracy}

# Function to start the Flower server
def start_flower_server():
    # Create a FedAvg strategy
    strategy = fl.server.strategy.FedAvg(min_fit_clients=2, min_evaluate_clients=2, min_available_clients=2)

    # Define server config with number of rounds
    server_config = fl.server.ServerConfig(num_rounds=3)

    # Start the federated learning server with the defined config
    print("Server: Starting Flower server...")
    fl.server.start_server(server_address="localhost:8080", strategy=strategy, config=server_config)

# Function to start the Flower client
def start_flower_client():
    time.sleep(2)
    model = build_model(X_train.shape[1])
    client = FLClient(model)

    print("Client: Starting client connection to the server...")
    fl.client.start_client(server_address="localhost:8080", client=client.to_client())

# Start a Federated Learning simulation with multiprocessing
if __name__ == "__main__":
    server_process = multiprocessing.Process(target=start_flower_server)
    client_process = multiprocessing.Process(target=start_flower_client)

    server_process.start()
    client_process.start()

    server_process.join()
    client_process.join()
