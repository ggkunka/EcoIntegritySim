# EcoIntegritySim

**EcoIntegritySim** is a simulation platform designed to ensure the integrity of environmental data using a combination of federated learning and blockchain technology. The project leverages AI-based anomaly detection and tamper-proof logging on a distributed ledger, making it suitable for environments requiring data redundancy and security.

## Features

- **Federated Learning**: Distributed machine learning model training without centralizing data.
- **Blockchain Integration**: Immutable logging of detected anomalies for traceability and security.
- **AI-based Anomaly Detection**: Detection of data anomalies using autoencoders.
- **Multi-agent System**: Implements a collaborative approach for model training and anomaly logging.

## Project Structure

```plaintext
EcoIntegritySim/
│
├── federated_learning_simulation.py    # Federated learning simulation script
├── ids.py                              # Anomaly detection using an autoencoder and blockchain logging
├── eco-integrity-contract/             # Smart contract for blockchain interactions
│   ├── contracts/                      # Solidity contracts
│   ├── migrations/                     # Migration files for deploying contracts
│   ├── build/                          # Compiled contracts and ABI
│   └── truffle-config.js               # Truffle configuration
├── run_blockchain_automation.sh        # Script to automate the blockchain and federated learning process
└── README.md                           # Project documentation

## Prerequisites

Before running the project, make sure you have the following installed:

- **Node.js** (v16.20.2)
- **Ganache CLI** (Blockchain simulation)
- **Truffle** (For deploying smart contracts)
- **Python** (Version 3.12 or later)
- **Conda** (To manage virtual environments)
- **TensorFlow** (For machine learning)

## Installation

### 1. **Clone the repository**:

```bash
git clone https://github.com/ggkunka/EcoIntegritySim.git
cd EcoIntegritySim

### 2. **Set up the environment:**:
Create and activate the conda environment:

```bash
conda create -n fresh-env python=3.12
conda activate fresh-env

### 3. **Install dependencies:**:

```bash

npm install -g ganache-cli
npm install -g truffle

## Usage

### 1. **Running the Blockchain Automation Script**

You can automate the process of starting the blockchain and federated learning by using the `run_blockchain_automation.sh` script:

```bash
./run_blockchain_automation.sh

This script:

Starts Ganache CLI.
Deploys the smart contracts.
Initiates the federated learning process.
Runs anomaly detection and logs detected anomalies to the blockchain.

## Project Goals

The key goals of this project are:

1. **Ensure Data Integrity**  
   Leverage blockchain technology to provide a robust and tamper-proof system for maintaining the integrity of environmental data.

2. **Enhance Anomaly Detection**  
   Implement AI-driven anomaly detection techniques to identify irregularities in environmental datasets, using machine learning models like autoencoders.

3. **Secure Logging**  
   Use smart contracts on a blockchain to securely log detected anomalies, ensuring that the logs are immutable and verifiable.

License
This project is licensed under the GNU General Public License v3.0. See the LICENSE file for more details.

Contributing
Contributions are welcome! Please open a pull request or issue to discuss changes or features.

Contact
For further questions or inquiries, feel free to reach out:

GitHub: https://github.com/ggkunka


