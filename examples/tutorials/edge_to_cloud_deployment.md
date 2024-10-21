# Edge-to-Cloud Deployment Tutorial

## Overview
This tutorial provides step-by-step instructions on deploying the **Decentralized AI System** across both edge devices and the cloud. The goal is to ensure a seamless interaction between edge nodes—such as IoT or ARM-based devices—and cloud infrastructure, enabling efficient distributed training and model deployment. This approach allows AI models to leverage the computational power of cloud environments while benefiting from real-time data collected by edge nodes.

## Prerequisites
### 1. System Requirements
- **Cloud Environment**: Access to a cloud provider such as AWS, Azure, or GCP.
- **Edge Device**: A resource-constrained device like a Raspberry Pi or NVIDIA Jetson Nano.
- **Docker**: Installed on both the cloud and edge devices.
- **Python 3.8+**: Installed on both environments.
- **Kubernetes (Optional)**: For managing deployments across multiple cloud nodes.

### 2. Required Configurations
- Ensure that the **edge deployment configurations** are defined in `configs/edge_config.yaml`.
- Cloud configurations are specified in `configs/cloud_config.yaml`.
- Download and set up **kubectl** and **docker-compose** for easier orchestration and container management.

## Step 1: Configure the Cloud Environment
### 1.1 Provision Cloud Resources
- **Virtual Machines**: Use cloud provider services (AWS EC2, Azure VMs, GCP Compute Engine) to set up the necessary compute resources.
  - Ensure each instance meets the minimum requirements (4 CPUs, 16 GB RAM).
  - Set up a virtual private cloud (VPC) to isolate the instances for security.

### 1.2 Deploy Core Orchestrator on Cloud
- The **orchestrator** is the central unit that manages communication between cloud and edge agents.
- Use Docker to deploy the orchestrator:
  ```sh
  docker-compose -f deployment/docker/compose.yml up orchestrator
  ```
- Alternatively, if Kubernetes is available, deploy the orchestrator with:
  ```sh
  kubectl apply -f deployment/kubernetes/deployment.yaml
  ```
- Verify that the orchestrator is running by accessing the health endpoint:
  ```
  curl http://<cloud-ip>:8001/health
  ```

### 1.3 Set Up Cloud Agent(s)
- Cloud agents provide additional computing power for training the models.
- Deploy agents to cloud instances using the cloud Dockerfile:
  ```sh
  docker build -t dai-agent-cloud -f deployment/docker/Dockerfile.cloud .
  docker run -d --name dai_agent_cloud --network host dai-agent-cloud
  ```

## Step 2: Set Up Edge Device(s)
### 2.1 Install Dependencies on Edge Device
- **Install Docker**: Install Docker on the edge device to manage containers.
  ```sh
  curl -fsSL https://get.docker.com -o get-docker.sh
  sh get-docker.sh
  ```
- **Python and Packages**: Install Python and other required libraries on the edge device:
  ```sh
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip
  pip3 install -r examples/edge_deployment/edge_agent_requirements.txt
  ```

### 2.2 Deploy the Edge Agent
- Configure the edge agent settings in `configure_edge.yaml` to specify orchestrator IP, model paths, and other parameters.
- Run the deployment script to start the edge agent:
  ```sh
  python examples/edge_deployment/deploy_edge_agent.py --config examples/edge_deployment/configure_edge.yaml
  ```
- The edge agent will register with the cloud orchestrator, and you can monitor its status in the orchestrator dashboard.

### 2.3 Test Connectivity
- Ensure that the edge agent can communicate with the cloud orchestrator:
  ```sh
  curl http://<cloud-orchestrator-ip>:8001/api/agents/status
  ```
  - The status should show the newly added edge agent.

## Step 3: Running Edge-to-Cloud Training
### 3.1 Shard Data Between Edge and Cloud
- Use the `data_sharder.py` utility to split the dataset between edge and cloud agents:
  ```sh
  python core/data/data_sharder.py --input data/mnist.csv --split 0.7 --output-edge data/edge_data.csv --output-cloud data/cloud_data.csv
  ```
- This ensures that the majority of data is processed at the edge, with the orchestrator aggregating results and managing overall training.

### 3.2 Initiate Training from Orchestrator
- From the orchestrator, send a request to all agents (cloud and edge) to initiate the training process:
  ```sh
  curl -X POST http://<cloud-orchestrator-ip>:8001/api/training/start
  ```
- Agents will start training using their respective datasets and communicate gradients to the orchestrator for aggregation.

## Step 4: Monitoring and Optimization
### 4.1 Monitor Training Progress
- **Grafana Dashboard**: Use Grafana to monitor metrics such as training accuracy, model loss, resource usage, and agent status.
  - Access Grafana at `http://<cloud-ip>:3000`.
  - Ensure that the Prometheus agent is scraping metrics from both cloud and edge nodes.

### 4.2 Resource Optimization
- **Batch Size and Epochs**: If training is taking too long on edge devices, consider reducing the **batch size** and **number of epochs** in `configs/performance_config.yaml`.
- **Auto-scaling Agents**: Enable Kubernetes auto-scaling for cloud agents by applying `autoscaler.yaml`.

### 4.3 Troubleshooting
- Check agent and orchestrator logs for any errors:
  - Edge logs: `logs/agents/edge_agent.log`
  - Cloud logs: `logs/orchestrator/orchestrator_main.log`
- If an agent disconnects, check network connectivity or resource exhaustion on the device.

## Step 5: Deploying the Trained Model
### 5.1 Aggregate the Model
- Once training completes, the orchestrator will aggregate all model updates and produce a final model.
- Save the model to a registry:
  ```sh
  curl -X POST -F 'model=@final_model.pth' http://<cloud-ip>:8001/api/models/upload
  ```

### 5.2 Deploy to Edge for Inference
- Convert the final model to **ONNX** for efficient inference on edge devices:
  ```sh
  python core/models/onnx_conversion.py --input final_model.pth --output final_model.onnx
  ```
- Deploy the ONNX model to the edge device:
  ```sh
  python examples/edge_deployment/deploy_edge_agent.py --model final_model.onnx
  ```
- The edge device can now use the model for local inference, leveraging the data it collects in real time.

## Summary
This tutorial provided a comprehensive guide to deploying the **Decentralized AI System** across both cloud and edge environments. By following the steps in this guide, you can successfully run distributed AI models that utilize the computational capabilities of the cloud while benefitting from real-time data collection at the edge.

### Key Highlights:
- Set up and deploy orchestrators in the cloud.
- Deploy agents on resource-constrained edge devices.
- Monitor distributed training progress using tools like Prometheus and Grafana.
- Aggregate and deploy models for inference across edge nodes.

For further customization or deployment-specific questions, please refer to the [Deployment Guide](deployment_guide.md) or reach out to the maintainers for support.

