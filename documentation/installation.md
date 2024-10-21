# Installation Guide

## Overview
This guide provides step-by-step instructions for installing and setting up the **Decentralized AI System** on your local environment, edge devices, or cloud infrastructure. The installation process includes setting up dependencies, configuring environment variables, and deploying the backend, frontend, and agent services.

## Prerequisites
Before installing the Decentralized AI System, make sure you have the following software and tools installed:

### 1. System Requirements
- **Operating System**: Linux (Ubuntu 18.04 or later recommended) or macOS
- **Python**: Version 3.8 or higher
- **Docker**: Version 19.03 or higher
- **Docker Compose**: Version 1.27 or higher
- **Node.js and npm**: Required for the frontend
- **Git**: Version control for cloning the repository

### 2. Optional Tools (For Cloud and Edge Deployments)
- **Kubernetes and kubectl**: For cloud container orchestration
- **Terraform**: For cloud infrastructure management
- **Ansible**: For managing edge device configurations
- **SSH Access**: Required for deploying to remote cloud or edge environments

## Step-by-Step Installation

### Step 1: Clone the Repository
First, clone the project repository from GitHub:
```bash
git clone https://github.com/your-username/dai_project.git
cd dai_project
```

### Step 2: Set Up Virtual Environment
It is recommended to create a Python virtual environment to isolate the dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies
Install the required Python packages for the backend:
```bash
pip install -r requirements.txt
```
For development purposes, also install the development dependencies:
```bash
pip install -r requirements_dev.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory to set up environment variables for the backend. This should include details like database connection strings, secret keys, and other configuration parameters.

Example `.env` file:
```env
DB_CONNECTION_STRING=mongodb://localhost:27017/dai_db
SECRET_KEY=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
```

### Step 5: Set Up Docker
Ensure Docker is installed and running. Navigate to the `deployment/docker/` directory to build and deploy the containers:

#### Step 5.1: Build Docker Images
For cloud deployment, you can build the Docker image using:
```bash
docker build -t dai-cloud -f Dockerfile.cloud .
```
For edge devices, use:
```bash
docker build -t dai-edge -f Dockerfile.edge .
```

#### Step 5.2: Run Docker Containers
Run the container using Docker Compose for easier orchestration:
```bash
docker-compose -f compose.yml up -d
```
This will start all necessary services such as the orchestrator, blockchain nodes, and agents.

### Step 6: Set Up the Frontend
Navigate to the `frontend/` directory to install and set up the FastAPI-based frontend:

#### Step 6.1: Install Frontend Dependencies
Install the necessary JavaScript packages using `npm`:
```bash
npm install
```

#### Step 6.2: Run the Frontend Server
Run the FastAPI server to start the frontend:
```bash
./run_frontend.sh
```
The frontend will be available at `http://localhost:8000`.

### Step 7: Initialize the Database
For initial setup, you may need to migrate the database to ensure that all tables are created. You can use the migration script available in the project:
```bash
./scripts/migrate.sh
```
This will initialize the database schema and set up the required tables.

### Step 8: Kubernetes Deployment (Optional)
If you are deploying the system in a Kubernetes cluster, navigate to the `deployment/kubernetes/` directory:
1. Deploy orchestrator and agent services:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```
2. Verify all pods are running:
   ```bash
   kubectl get pods
   ```

### Step 9: Edge Device Deployment (Optional)
For edge deployment, use Ansible to set up the edge environment:
1. Navigate to the `deployment/ansible/` directory.
2. Run the Ansible playbook for edge setup:
   ```bash
   ansible-playbook -i inventory playbook_edge.yml
   ```

### Step 10: Monitoring Setup
To set up monitoring and visualize metrics:
1. Navigate to `examples/federated_dashboard/`.
2. Start the monitoring dashboard:
   ```bash
   ./start_dashboard.sh
   ```
You can access the Grafana dashboard through the provided URL for real-time monitoring of the system's performance and agent activities.

---

## Post Installation
### Verifying the Setup
- **Backend**: Verify that the backend is running by accessing the API documentation at `http://localhost:8000/docs`.
- **Frontend**: Ensure that the user interface loads correctly by navigating to `http://localhost:8000`.
- **Agents and Orchestrators**: Use the Kubernetes or Docker commands to ensure all containers and pods are up.

### Initial Testing
- Run the unit tests to verify the initial setup:
  ```bash
  pytest core/tests/unit_tests/
  ```
- If the tests pass successfully, your installation is ready.

## Troubleshooting
- **Docker Issues**: Ensure Docker has sufficient memory allocated. Increase Docker memory limits in settings if containers fail to start.
- **Environment Variables**: Ensure all necessary environment variables are set correctly. Incorrect configurations can prevent services from starting.
- **Database Connection**: Ensure the database connection string is correct in the `.env` file. The system will not run if it cannot connect to the database.

## Summary
The installation guide provides all the necessary steps to set up the Decentralized AI System in different environments, including local, cloud, and edge devices. After installation, you can proceed to explore the features of the system, deploy agents, and train models in a decentralized manner.

If you have any issues during the installation, refer to the [Troubleshooting Guide](troubleshooting.md) or seek help through our community discussions.

