# Federated Learning Tutorial

## Overview
**Federated Learning** is a technique that allows AI models to be trained across multiple decentralized devices or servers while keeping the data on the device, ensuring privacy and data security. This tutorial walks you through the steps required to set up and execute a federated learning workflow using the **Decentralized AI System**. This approach allows multiple nodes (edge devices, mobile phones, or remote servers) to participate in a collaborative training process without sharing raw data.

## Prerequisites
### 1. System Requirements
- **Python 3.8+**: Ensure you have the latest Python version installed.
- **Docker**: Install Docker for managing containers across nodes.
- **Edge Devices or Virtual Machines**: Any devices that can serve as participants in federated learning (e.g., Raspberry Pi, desktops, or VMs).
- **Kubernetes (Optional)**: If you are orchestrating a large number of federated learning agents.
- **Node.js**: Required if you are using the web-based frontend for controlling the federated learning process.

### 2. Setup Steps
- **Clone the Repository**: Clone the **Decentralized AI System** repository and install dependencies:
  ```sh
  git clone https://github.com/your-repository/dai_project.git
  cd dai_project
  pip install -r requirements.txt
  ```
- **Edge Configuration**: Make sure that edge devices have appropriate configurations for participating in federated learning. These settings can be defined in `configs/edge_config.yaml`.

## Step 1: Setting Up the Federated Orchestrator
The orchestrator manages and coordinates the federated learning process, ensuring that updates are collected from all nodes, aggregated securely, and distributed back to participants.

### 1.1 Deploy the Orchestrator
- Start the orchestrator using Docker Compose:
  ```sh
  docker-compose up orchestrator
  ```
- Alternatively, use Kubernetes for large-scale deployments:
  ```sh
  kubectl apply -f deployment/kubernetes/deployment.yaml
  ```
- Verify the orchestrator is running by accessing the health endpoint at:
  ```
  curl http://<orchestrator-ip>:8001/health
  ```

## Step 2: Registering Participants
### 2.1 Set Up Participating Nodes
- Each participating device (or node) needs to run an agent that will participate in federated learning. Use Docker to deploy agents:
  ```sh
  docker-compose up agent
  ```
- For edge devices, use:
  ```sh
  python examples/edge_deployment/deploy_edge_agent.py --config examples/edge_deployment/configure_edge.yaml
  ```
- Agents will automatically register with the orchestrator and appear in the dashboard available at `http://<orchestrator-ip>:8001/agents`.

### 2.2 Authentication of Participants
- Each node must authenticate with the orchestrator using a token issued by the **identity_management** module (`core/agents/identity_management.py`). Generate tokens with:
  ```sh
  python core/agents/identity_management.py --generate-token --agent-id <agent_name>
  ```

## Step 3: Running Federated Learning
### 3.1 Start Federated Training
- From the orchestrator dashboard, initiate the training process by selecting the desired model and dataset (e.g., **MNIST**).
- You can start federated training from the command line as well:
  ```sh
  curl -X POST http://<orchestrator-ip>:8001/api/training/start
  ```

### 3.2 Local Training at Edge Devices
- Each participating agent trains the model locally using its own dataset. Training parameters such as **batch size** and **learning rate** can be configured in `configs/performance_config.yaml`.
- Agents report updates to the orchestrator upon completing local training.

### 3.3 Secure Aggregation
- The orchestrator aggregates updates securely using **Secure Multiparty Computation (MPC)** and **Homomorphic Encryption**. This ensures that no individual agent can see the data or model updates from other agents.
- The aggregated model is then redistributed to participating nodes for the next round of training.

## Step 4: Monitoring Training Progress
### 4.1 Dashboard Monitoring
- Use the Grafana dashboard to monitor the federated training progress:
  - Access the dashboard at `http://<orchestrator-ip>:3000`.
  - Monitor key metrics such as **training accuracy**, **model loss**, and **agent status**.

### 4.2 Anomaly Detection
- Logs are collected and monitored for anomalies. Alerts are configured via **Prometheus** to trigger notifications if a participating node deviates significantly from expected behavior.

## Step 5: Deploying the Trained Model
### 5.1 Model Aggregation and Finalization
- Once federated learning completes, the orchestrator aggregates the final model and saves it to the model registry.
  ```sh
  curl -X POST -F 'model=@final_model.pth' http://<orchestrator-ip>:8001/api/models/upload
  ```

### 5.2 Edge Deployment
- Convert the trained model to **ONNX** format for efficient deployment on edge devices:
  ```sh
  python core/models/onnx_conversion.py --input final_model.pth --output model.onnx
  ```
- Deploy the ONNX model to edge devices for inference.
  ```sh
  python examples/edge_deployment/deploy_edge_agent.py --model model.onnx
  ```

## Security Considerations
### 6.1 Differential Privacy
- Differential privacy can be enabled to ensure that no private information about training data is leaked during model updates. Set `differential_privacy: true` in `configs/privacy_config.yaml`.

### 6.2 Identity Verification
- Each participating agent must be authenticated to prevent unauthorized devices from joining the federated network.
- Tokens generated by the **identity_management** module should be kept secure and rotated periodically.

## Performance Tuning
### 7.1 Batch Size and Learning Rate
- Optimize the **batch size** and **learning rate** based on the computational capabilities of participating devices. Devices with fewer resources should use smaller batch sizes.

### 7.2 Parallelism and Scaling
- Configure the **number of parallel agents** in `configs/performance_config.yaml` to ensure that multiple agents can participate simultaneously.
- Kubernetes can be used for dynamic scaling if many agents need to be orchestrated.

## Troubleshooting
- If an agent fails to send updates:
  - Check network connectivity between the agent and orchestrator.
  - Review logs located in `logs/agents/agent_1.log` for specific errors.
- **High Resource Usage**: If training is slow or resource consumption is high on edge devices, reduce the batch size or consider quantizing the model.

## Summary
This **Federated Learning Tutorial** provides all the necessary steps to set up and run a federated learning workflow using the **Decentralized AI System**. By following the instructions in this guide, you can distribute model training across multiple devices while preserving data privacy.

### Key Takeaways
- Set up and deploy orchestrators and agents to participate in federated learning.
- Securely aggregate model updates without sharing raw data using secure aggregation techniques.
- Monitor training progress using Grafana and deploy the trained model to edge devices for inference.

For additional information, refer to the [Privacy Guide](privacy_policy.md) or [Edge-to-Cloud Deployment Tutorial](edge_to_cloud_deployment.md) for specific deployment scenarios.

