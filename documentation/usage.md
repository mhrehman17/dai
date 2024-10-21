# Usage Guide

## Overview
This **Usage Guide** provides step-by-step instructions on how to use the **Decentralized AI System** for training and deploying AI models. It covers setting up agents, orchestrators, deploying models, managing model versions, and using the monitoring tools to track system performance. By following this guide, you will be able to run training workflows across distributed systems, deploy AI models on cloud and edge nodes, and utilize privacy and performance features effectively.

## Getting Started
### 1. Prerequisites
- **Python 3.8+**: Ensure you have Python installed.
- **Docker**: Install Docker for containerized deployment.
- **Kubernetes** (Optional): For orchestrating multiple agents across different nodes.
- **Node.js**: Needed if you are working with the web-based frontend.
- **System Dependencies**: Install required dependencies by running:
  ```sh
  pip install -r requirements.txt
  ```
  For development purposes, use `requirements_dev.txt` for additional dependencies.

### 2. Setting Up the Environment
- Clone the repository and navigate to the project directory:
  ```sh
  git clone https://github.com/your-repository/dai_project.git
  cd dai_project
  ```
- **Configure Environment Variables**: Set up environment variables for system settings. Create a `.env` file with the following information:
  ```env
  ORCHESTRATOR_ENDPOINT=http://localhost:8001
  DATABASE_URL=postgresql://user:password@localhost/dbname
  ```
- **Start Supporting Services**: If using Kubernetes, deploy orchestrators and agents using the provided configurations:
  ```sh
  kubectl apply -f deployment/kubernetes/deployment.yaml
  ```
- **Database Setup**: Initialize the database schema by running:
  ```sh
  ./scripts/migrate.sh
  ```

## Running Core Components
### 3. Start Orchestrator
The orchestrator manages distributed training and coordinates agents.
- Run the orchestrator using Docker Compose:
  ```sh
  docker-compose up orchestrator
  ```
- Alternatively, use Kubernetes:
  ```sh
  kubectl apply -f deployment/kubernetes/orchestrator.yaml
  ```
- Verify the orchestrator is running by visiting: `http://localhost:8001/health`

### 4. Deploy Agents
Agents perform model training tasks and send updates to the orchestrator.
- To deploy agents:
  ```sh
  docker-compose up agent
  ```
- If deploying to edge devices, use the edge deployment script:
  ```sh
  python examples/edge_deployment/deploy_edge_agent.py --config configs/edge_config.yaml
  ```

### 5. Using the Model Registry
- **Upload Model**: Use the API to upload new models.
  ```sh
  curl -X POST -F 'model=@path/to/model.pth' http://localhost:8001/api/models/upload
  ```
- **List Available Versions**: To list all available model versions, use the following endpoint:
  ```sh
  curl http://localhost:8001/api/models/versions
  ```

### 6. Starting the Frontend Interface
The **frontend** provides a web-based interface to manage agents, orchestrators, model versions, and monitor metrics.
- Navigate to the `frontend` directory and run:
  ```sh
  ./run_frontend.sh
  ```
- Once the server is running, visit `http://localhost:3000` to access the frontend.
- Log in with the default credentials (`admin` / `admin`). You can change these later for better security.

## Training and Deployment Workflow
### 7. Training a Model
- **Start Training**: From the frontend, go to the **Training** section, choose the dataset (e.g., MNIST), and select parameters like **batch size** and **number of epochs**.
- **Agent Assignment**: The orchestrator will automatically assign tasks to available agents.
- **Monitor Training**: Monitor the status of training in the **Metrics** section or **Training Dashboard**.

### 8. Deploying a Model to Edge Devices
- **Convert to ONNX**: For edge deployments, convert the trained model to ONNX format using the `onnx_conversion.py` script:
  ```sh
  python core/models/onnx_conversion.py --input trained_model.pth --output model.onnx
  ```
- **Deploy**: Deploy the converted ONNX model using `deploy_edge_agent.py`:
  ```sh
  python examples/edge_deployment/deploy_edge_agent.py --model model.onnx
  ```

## Managing Privacy and Security
### 9. Privacy Features
- **Differential Privacy**: Enable differential privacy during training by setting `differential_privacy: true` in `configs/privacy_config.yaml`.
- **Homomorphic Encryption**: Use homomorphic encryption during aggregation for additional privacy.
- **Privacy Metrics**: Track privacy metrics using the **Privacy Monitor** accessible through the frontend.

### 10. Authentication and Authorization
- **User Authentication**: Use the **authentication** endpoint (`frontend/api/endpoints/authentication.py`) for managing user login and token issuance.
- **Zero Trust Architecture**: Set up identity verification for agents using the `identity_utils.py` module to enforce secure communication.

## Monitoring and Debugging
### 11. Metrics and Dashboards
- **View Metrics**: Use the Grafana dashboard to monitor training metrics, agent status, system resource usage, etc.
  - Access Grafana at `http://localhost:3000`.
- **Log Collection**: Use the `log_collector.py` script to collect logs from different components:
  ```sh
  python core/monitoring/log_collector.py
  ```
- **Alerts**: Configure alerts in Prometheus to notify when CPU/memory usage exceeds certain thresholds.

### 12. Troubleshooting Issues
If there are issues in the system:
- Check logs under the `logs/` directory for relevant components (e.g., `logs/agents/`, `logs/orchestrator/`).
- Refer to the [Troubleshooting Guide](troubleshooting.md) for detailed solutions to common issues.

## Performance Optimization
### 13. Performance Tuning
- **Batch Size and Epochs**: Adjust the `batch_size` and `num_epochs` in `configs/performance_config.yaml` for optimal training speed.
- **Auto-Scaling**: Enable auto-scaling in Kubernetes by applying `autoscaler.yaml` to dynamically adjust the number of agents.
- **Model Quantization**: Reduce model complexity using the `model_quantization.py` script, which improves performance for edge deployments.

## Running Tests
### 14. Running Unit and Integration Tests
- **Unit Tests**: Navigate to the `core/tests/unit_tests/` directory and run:
  ```sh
  pytest
  ```
- **Integration Tests**: Run integration tests to ensure that different components are working together as expected:
  ```sh
  pytest core/tests/integration_tests/
  ```
- **Load Testing**: Use the `performance_tests.sh` script to simulate high-load scenarios and identify potential bottlenecks.

## Best Practices for Usage
1. **Start Small**: Begin with a minimal number of agents and gradually scale as you become comfortable with the orchestration processes.
2. **Enable Logs**: Always enable detailed logging during initial deployments. This makes troubleshooting easier if unexpected issues occur.
3. **Security Settings**: Configure privacy settings from the start, especially when dealing with sensitive data. Use differential privacy and encryption to minimize privacy risks.
4. **Regularly Update Models**: Use the model registry to keep models up-to-date. Periodically replace older models with newer versions as more data becomes available.

## Summary
This **Usage Guide** helps users get started with the **Decentralized AI System** for training, managing, and deploying AI models across distributed environments. The guide covers setting up services, training workflows, managing model versions, enabling privacy, and monitoring system performance to ensure the system is running smoothly and efficiently.

For more information on advanced configurations, refer to the [Deployment Guide](deployment_guide.md) or [Monitoring Guide](monitoring_guide.md).

