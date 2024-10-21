#!/bin/bash

# This script runs performance tests for the decentralized AI system.
# It uses Locust to perform load testing on the API endpoints to evaluate performance under different load conditions.

# Check if Locust is installed
if ! command -v locust &> /dev/null
then
    echo "Locust could not be found. Please make sure all dependencies are installed by running:"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Define environment variables for Locust testing
LOCUST_FILE=${LOCUST_FILE:-"locustfile.py"}
HOST_URL=${HOST_URL:-"http://localhost:8000"}
USERS=${USERS:-100}
SPAWN_RATE=${SPAWN_RATE:-10}

# Check if Locust test file exists
if [ ! -f "$LOCUST_FILE" ]; then
    echo "Error: Locust file '$LOCUST_FILE' not found. Please ensure the locustfile is present."
    exit 1
fi

# Run Locust performance test
locust -f "$LOCUST_FILE" --host "$HOST_URL" --users "$USERS" --spawn-rate "$SPAWN_RATE" --headless -t 5m

if [ $? -eq 0 ]; then
    echo "Performance tests completed successfully."
else
    echo "Error: Performance testing failed."
    exit 1
fi

# Completion message
echo "Performance testing completed. Results available in the Locust web interface or summary report."
