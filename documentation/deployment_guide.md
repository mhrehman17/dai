# Deployment Guide

## Overview
This guide will walk you through the steps needed to deploy the Decentralized AI System on different environments including cloud, edge devices, and hybrid cloud-edge setups. The system is designed for scalability, privacy preservation, and ease of management through containerized deployment using Docker, Kubernetes, and other Infrastructure as Code (IaC) tools like Terraform and Ansible.

## Deployment Scenarios
1. **Cloud Deployment**: Ideal for centralized data processing, high scalability, and resource availability.
2. **Edge Deployment**: Suitable for local data processing, privacy-preserving scenarios, and real-time analysis.
3. **Hybrid Deployment**: Combines the benefits of cloud and edge for both resource efficiency and privacy.

---

## Prerequisites
- **Docker** and **Docker Compose** installed on the deployment machine.
- **Kubernetes** and **kubectl** command-line tool installed (for cloud deployments).
- **Terraform** installed for Infrastructure as Code setup.
- **Ansible** installed for configuring and managing remote edge devices.
- **SSH Access** to cloud servers or edge devices.

---

## 1. Cloud Deployment
### Step 1: Provision Cloud Infrastructure
Use **Terraform** to provision cloud resources on AWS, Azure, or Google Cloud.
1. Navigate to the `deployment/terraform/` directory.
2. Edit the `variables.tf` file to set the appropriate values for your cloud provider, region, instance type, and other settings.
3. Run the following commands to deploy:
   ```bash
   terraform init
   terraform apply
   ```
4. Confirm the creation plan. The infrastructure will be created as per the defined resources.

### Step 2: Deploy Services on Kubernetes
1. Navigate to the `deployment/kubernetes/` directory.
2. Apply the Kubernetes resources:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f blockchain_deployment.yaml
   kubectl apply -f blockchain_autoscaler.yaml
   ```
3. Use the `kubectl get pods` command to verify that all services are up and running.

### Step 3: Configure Load Balancer
The load balancer configuration is managed by Kubernetes using the `service.yaml` file.
- To get the external IP address of the load balancer, run:
  ```bash
  kubectl get service dai-load-balancer
  ```
- Access the system using the external IP address obtained above.

---

## 2. Edge Deployment
### Step 1: Set Up Edge Devices
Use **Ansible** to configure edge devices like Raspberry Pi.
1. Ensure the edge device is connected to the network and accessible via SSH.
2. Navigate to the `deployment/ansible/` directory.
3. Edit the `inventory` file to add the IP addresses of your edge devices.
4. Run the following playbook to configure the devices:
   ```bash
   ansible-playbook -i inventory playbook_edge.yml
   ```
5. This playbook will install Docker, configure the edge environment, and deploy the required containers.

### Step 2: Deploy Edge Agents
1. SSH into the edge device.
2. Navigate to the `deployment/docker/` directory and run the Docker container:
   ```bash
   docker build -t edge-agent -f Dockerfile.edge .
   docker run -d --name edge_agent edge-agent
   ```
3. Verify the deployment by checking the logs:
   ```bash
   docker logs edge_agent
   ```

---

## 3. Hybrid Deployment
The hybrid deployment approach leverages both cloud resources for model orchestration and edge devices for local data processing.

### Step 1: Set Up Cloud Resources
Follow the steps outlined in **Cloud Deployment** to provision the cloud infrastructure.

### Step 2: Configure Edge Agents
Follow the steps in **Edge Deployment** to deploy edge agents on edge devices.

### Step 3: Connect Edge Agents to Cloud Orchestrator
1. Configure the orchestrator URL in `configure_edge.yaml` file located in `deployment/edge_deployment/`.
2. Update each edge agent with the orchestrator's public IP so that they can connect and send model updates securely.
3. Restart the edge agent container:
   ```bash
   docker restart edge_agent
   ```

---

## Deployment Verification
### Kubernetes Dashboard
- Use the Kubernetes Dashboard to verify that all pods, deployments, and services are functioning properly.
- Access the dashboard:
  ```bash
  kubectl proxy
  ```
  Open the Kubernetes Dashboard at `http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/`.

### Metrics Monitoring
- Use **Prometheus** and **Grafana** for monitoring. The metrics dashboard can be started by navigating to `examples/federated_dashboard/` and running:
  ```bash
  ./start_dashboard.sh
  ```
- The Grafana dashboard can be accessed through the provided URL on startup.

### Logs
- All logs are collected and centralized in the `logs/` directory.
- Logs for specific components (e.g., blockchain, agents, orchestrator) can be accessed individually:
  ```bash
  tail -f logs/agents/agent_1.log
  ```

---

## Updating Deployments
- **Rolling Update**: For Kubernetes-based deployments, use the following command to perform a rolling update to the orchestrator or agents:
  ```bash
  kubectl set image deployment/dai-orchestrator orchestrator-container=dai-system/orchestrator:latest
  ```
- **Edge Update**: For edge devices, re-run the Ansible playbook to push updates:
  ```bash
  ansible-playbook -i inventory playbook_edge.yml
  ```

---

## Troubleshooting
1. **Pod Crashing**: Check pod logs for error messages:
   ```bash
   kubectl logs <pod-name>
   ```
2. **Agent Not Connecting**: Verify that the agent has the correct orchestrator IP configured.
3. **Performance Issues**: Check resource usage with Prometheus and adjust auto-scaling configurations in `blockchain_autoscaler.yaml`.

## Summary
This guide provides all the steps required to successfully deploy the Decentralized AI System across various environments, including cloud, edge, and hybrid deployments. Make sure to verify each component's functionality and refer to the monitoring and logging sections for ongoing system maintenance.

For additional details or to contribute, refer to the other sections of the documentation.

