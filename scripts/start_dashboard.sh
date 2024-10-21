#!/bin/bash

# This script starts the interactive monitoring dashboard for the decentralized AI system.
# It uses Streamlit to launch a web-based dashboard that provides metrics and monitoring information.

# Define environment variables for the dashboard
DASHBOARD_SCRIPT="frontend/dashboard.py"
DASHBOARD_PORT=${DASHBOARD_PORT:-8501}

# Check if Streamlit is installed
if ! command -v streamlit &> /dev/null
then
    echo "Streamlit could not be found. Please make sure all dependencies are installed by running:"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Check if the dashboard script exists
if [ ! -f "$DASHBOARD_SCRIPT" ]; then
    echo "Error: Dashboard script '$DASHBOARD_SCRIPT' not found. Please ensure the script is available."
    exit 1
fi

# Run the Streamlit dashboard
streamlit run "$DASHBOARD_SCRIPT" --server.port="$DASHBOARD_PORT"

if [ $? -eq 0 ]; then
    echo "Dashboard is running successfully at http://localhost:$DASHBOARD_PORT"
else
    echo "Error: Failed to start the dashboard."
    exit 1
fi

# Completion message
echo "Dashboard started successfully. Press Ctrl+C to stop."
