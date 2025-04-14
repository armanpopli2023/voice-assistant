#!/bin/bash

# Exit on error
set -e

# Function to create and activate virtual environment
setup_venv() {
    local env_name=$1
    local venv_path="venv_${env_name}"
    
    echo "Setting up ${env_name} environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "$venv_path" ]; then
        echo "Creating virtual environment at ${venv_path}..."
        python -m venv "$venv_path"
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source "${venv_path}/bin/activate"
    
    # Upgrade pip
    echo "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    echo "Installing requirements..."
    pip install -r "requirements/${env_name}.txt"
    
    # Install webrtcvad (special handling for macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Installing webrtcvad for macOS..."
        pip install webrtcvad
    fi
    
    echo "Environment setup complete!"
    echo "To activate the environment, run: source ${venv_path}/bin/activate"
}

# Check if environment name is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 [development|production]"
    exit 1
fi

# Validate environment name
if [[ "$1" != "development" && "$1" != "production" ]]; then
    echo "Error: Environment must be either 'development' or 'production'"
    exit 1
fi

# Run setup
setup_venv "$1" 