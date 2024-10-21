#!/bin/bash

# This script sets up the development environment for the decentralized AI system project.
# It installs required dependencies, sets up virtual environments, and installs tools for development and testing.

# Define environment variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
REQUIREMENTS_DEV_FILE="requirements_dev.txt"

# Function to create a virtual environment
create_virtualenv() {
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        python3 -m venv "$VENV_DIR"
        echo "Virtual environment created at $VENV_DIR"
    else
        echo "Virtual environment already exists at $VENV_DIR"
    fi
}

# Function to activate the virtual environment
activate_virtualenv() {
    if [ -d "$VENV_DIR" ]; then
        echo "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
        echo "Virtual environment activated."
    else
        echo "Error: Virtual environment not found. Please run the script again to create it."
        exit 1
    fi
}

# Function to install dependencies
install_dependencies() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Installing project dependencies..."
        pip install -r "$REQUIREMENTS_FILE"
        echo "Project dependencies installed successfully."
    else
        echo "Error: Requirements file ($REQUIREMENTS_FILE) not found."
        exit 1
    fi

    if [ -f "$REQUIREMENTS_DEV_FILE" ]; then
        echo "Installing development dependencies..."
        pip install -r "$REQUIREMENTS_DEV_FILE"
        echo "Development dependencies installed successfully."
    else
        echo "Error: Development requirements file ($REQUIREMENTS_DEV_FILE) not found."
        exit 1
    fi
}

# Function to install pre-commit hooks
setup_pre_commit() {
    if command -v pre-commit &> /dev/null; then
        echo "Setting up pre-commit hooks..."
        pre-commit install
        echo "Pre-commit hooks set up successfully."
    else
        echo "Pre-commit not found. Installing pre-commit..."
        pip install pre-commit
        pre-commit install
        echo "Pre-commit hooks set up successfully."
    fi
}

# Main script execution
create_virtualenv
activate_virtualenv
install_dependencies
setup_pre_commit

# Completion message
echo "Development environment setup completed successfully. Activate the virtual environment using: source $VENV_DIR/bin/activate"
