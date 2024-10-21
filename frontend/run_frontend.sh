#!/bin/bash

# This script starts the FastAPI server for the frontend of the Decentralized AI System.

# Set environment variables if required (optional)
export UVICORN_WORKERS=4
export APP_HOST="0.0.0.0"
export APP_PORT=8000

# Check if the required Python dependencies are installed
if ! command -v uvicorn &> /dev/null
then
    echo "uvicorn could not be found. Please make sure all dependencies are installed by running:"
    echo "pip install -r requirements.txt"
    exit
fi

# Run the FastAPI application with Uvicorn
# --reload is useful for development, remove for production deployment
uvicorn api.main:app --host $APP_HOST --port $APP_PORT --workers $UVICORN_WORKERS --reload

# Optional: Add a message to indicate the server has started
echo "Frontend server is running at http://$APP_HOST:$APP_PORT"
