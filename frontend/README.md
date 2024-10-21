# Decentralized AI System - Frontend Setup

This README provides instructions to set up and run the FastAPI server for the frontend of the Decentralized AI System.

## Prerequisites

Before running the script, ensure that you have the following installed:

1. **Python 3.8 or higher**
2. **pip** (Python package manager)
3. **Uvicorn** - This can be installed through the `requirements.txt` file.
4. **Bash** - To run the provided shell script.

## Installation Steps

1. Clone the project repository:
   ```bash
   git clone <repository-url>
   cd dai_project/frontend
   ```
2. Install required Python dependencies:
```bash
   pip install -r requirements.txt
```
## Running the Frontend Server

To run the frontend server, use the provided run_frontend.sh script.

1. Make the script executable (if it isn't already):
```bash
chmod +x run_frontend.sh
```
2. Run the script to start the FastAPI server:
```bash
./run_frontend.sh
```

### Script Details
- The script starts the FastAPI server using Uvicorn.
- Environment variables used by the script:

UVICORN_WORKERS: Number of worker processes to handle requests. Default is set to 4.

APP_HOST: Host address to bind the server. Default is 0.0.0.0 (all available addresses).

APP_PORT: Port to run the server on. Default is 8000.

The script also checks if Uvicorn is installed and prompts for installation if not found.

### Development vs. Production
The script runs the server with --reload for automatic reloading during development.

For production, remove the --reload flag and consider using a production-ready server setup like Gunicorn.

Accessing the Frontend

After running the script, the frontend will be accessible at:

http://localhost:8000

or

http://0.0.0.0:8000 if accessed from a different machine in the network.

### Troubleshooting
Port Already in Use: If the default port (8000) is already in use, change the APP_PORT environment variable in the script.

Permission Denied: If you get a permission error when running the script, make sure it has executable permissions (chmod +x run_frontend.sh).

Dependencies Not Installed: If Uvicorn or other required dependencies are not installed, ensure you have successfully run pip install -r requirements.txt.

### Further Information

For more detailed information, please refer to the project documentation or reach out to the maintainers.