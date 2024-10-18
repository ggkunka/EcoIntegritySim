#!/bin/zsh

# Exit on error
set -e

# Set the Conda environment name
CONDA_ENV_NAME="fresh-env"

# Initialize Conda for zsh
echo "Initializing Conda..."
eval "$(conda shell.zsh hook)"

# Activate the Conda environment
echo "Activating Conda environment: $CONDA_ENV_NAME"
conda activate "$CONDA_ENV_NAME"

# Confirm activation
echo "Conda environment activated: $(conda info --envs | grep '*' | awk '{print $1}')"

# Initialize nvm to ensure the correct Node.js version is loaded
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Load the correct Node.js version using nvm
nvm use 16

# Check if port 8545 is being used
PORT=8545
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "Port $PORT is in use, terminating the process."
    kill -9 $(lsof -t -i :$PORT)
fi

# Start Ganache CLI and store its PID for later termination
echo "Starting Ganache CLI..."
ganache-cli --gasLimit 8000000 &
GANACHE_PID=$!

# Wait a few seconds for Ganache to start
sleep 5

# Navigate to the Truffle project directory
PROJECT_DIR="/Users/jayaprakash/EcoIntegritySim/eco-integrity-contract"
echo "Navigating to Truffle project directory: $PROJECT_DIR"
cd $PROJECT_DIR

# Deploy smart contract using Truffle
echo "Deploying smart contract using Truffle..."
TRUFFLE_OUTPUT=$(npx truffle migrate --network development)

# Extract contract address and network ID using standard grep and awk
CONTRACT_ADDRESS=$(echo "$TRUFFLE_OUTPUT" | grep 'contract address:' | awk '{print $4}')
NETWORK_ID=$(echo "$TRUFFLE_OUTPUT" | grep 'Network id:' | awk '{print $4}')

echo "Extracted Contract Address: $CONTRACT_ADDRESS"
echo "Extracted Network ID: $NETWORK_ID"

# Check if the network ID was extracted correctly
if [[ -z "$NETWORK_ID" || "$NETWORK_ID" == "id:" ]]; then
    echo "Error: Network ID could not be extracted. Exiting..."
    kill $GANACHE_PID
    exit 1
fi

# Running ids.py with extracted contract address and network ID
echo "Running ids.py..."
python /Users/jayaprakash/EcoIntegritySim/ids.py --contract_address $CONTRACT_ADDRESS --network_id $NETWORK_ID

# Clean up by stopping Ganache CLI
echo "Stopping Ganache CLI..."
kill $GANACHE_PID
