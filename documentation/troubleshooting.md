# Troubleshooting Guide

## Overview
This **Troubleshooting Guide** is designed to help you resolve common issues that might arise while using the **Decentralized AI System**. The guide addresses various components, including agents, orchestrators, blockchain nodes, model registry, and more. Each section includes potential problems, symptoms, and steps to identify and resolve issues efficiently.

## General Troubleshooting Steps
Before diving into specific issues, follow these general troubleshooting steps:
1. **Check System Logs**: Most issues can be identified using logs. Check logs in the `logs/` directory for specific services (e.g., `logs/agents/agent_1.log`).
2. **Restart Services**: If a service is behaving unexpectedly, try restarting it using Docker or Kubernetes commands.
3. **Check Dependencies**: Ensure all dependencies are installed as per the `requirements.txt` or `edge_agent_requirements.txt` file.
4. **Verify Network Connectivity**: Confirm that all services can communicate with each other, especially if there are connectivity issues.

## Common Issues and Solutions

### 1. Agent Not Registering with Orchestrator
**Symptoms**: Agents fail to register, and orchestrator logs show missing agent connections.

**Possible Causes**:
- **Network Issues**: The agent cannot reach the orchestrator due to firewall rules or incorrect network configuration.
- **Configuration Errors**: The agent configuration file has incorrect orchestrator endpoints.

**Solution**:
1. **Verify Network**: Run `ping orchestrator_ip` from the agent to verify that the agent can reach the orchestrator.
2. **Update Configuration**: Open the agent's configuration (`configs/agent_config.yaml`) and verify the orchestrator endpoint is correct.
3. **Logs**: Check `logs/agents/agent_1.log` and `logs/orchestrator/orchestrator_main.log` for detailed errors.

### 2. Orchestrator Fails to Aggregate Updates
**Symptoms**: Model aggregation fails, and training stalls with no new updates.

**Possible Causes**:
- **Agent Disconnection**: One or more agents disconnected during the update.
- **Incorrect Aggregation Strategy**: The aggregation strategy is incorrectly configured.

**Solution**:
1. **Check Agent Health**: View agent logs (`logs/agents/`) to see if any agents dropped out during training.
2. **Update Aggregation Strategy**: Open `configs/orchestrator_config.yaml` and adjust the aggregation strategy if needed.
3. **Fallback Orchestrator**: Check `logs/orchestrator/backup_orchestrator.log` to determine if the fallback orchestrator attempted aggregation.

### 3. Blockchain Node Not Syncing
**Symptoms**: The blockchain node does not seem to be syncing properly, causing transactions to stall.

**Possible Causes**:
- **Outdated Blockchain Data**: The node data is outdated or corrupted.
- **Consensus Issues**: A consensus mechanism issue such as missing validators.

**Solution**:
1. **Update Node**: Stop the node, clear the outdated blockchain data (`core/ledger/node_setup/`), and restart using the latest snapshot.
2. **Validator Setup**: Verify validator nodes are online using `core/ledger/node_setup/validator_node.py`.
3. **Logs**: Review `logs/blockchain/blockchain_node_1.log` for detailed syncing information.

### 4. Model Version Not Found During Deployment
**Symptoms**: Deployment fails with an error that the specified model version is not available.

**Possible Causes**:
- **Incorrect Version ID**: The version ID specified for deployment does not exist in the registry.
- **Model Registry Connection Issue**: The orchestrator cannot connect to the model registry.

**Solution**:
1. **Verify Version ID**: Run `GET /api/models/versions` through the API to list all available versions.
2. **Model Registry Connection**: Verify network connectivity between orchestrator and model registry (`logs/model_registry/model_versioning.log`).
3. **Fallback Version**: Use an earlier, stable version from `core/models/registry/storage/version_1/` if necessary.

### 5. High Resource Usage on Edge Device
**Symptoms**: CPU or memory usage spikes on edge agents, leading to degraded performance.

**Possible Causes**:
- **Large Batch Size**: The batch size may be too large for the available resources.
- **Resource Limit Exceeded**: The CPU or memory limit set in `performance_config.yaml` is too high.

**Solution**:
1. **Reduce Batch Size**: Open `configs/performance_config.yaml` and reduce the `batch_size` value for training agents.
2. **Set Limits**: Update Kubernetes resource limits in `deployment/kubernetes/deployment.yaml` to control resource consumption on edge nodes.
3. **Logs**: Check `logs/system_monitor/resource_usage.log` for detailed profiling information.

### 6. Orchestrator Not Scaling Properly
**Symptoms**: Agents are not scaling up even when CPU usage is high.

**Possible Causes**:
- **HPA Misconfiguration**: Horizontal Pod Autoscaler (HPA) settings are not correctly configured.
- **Auto-scaling Disabled**: The `auto_scaling_enabled` setting in `performance_config.yaml` is set to false.

**Solution**:
1. **Check HPA Status**: Run `kubectl get hpa` to see if the HPA is configured and active.
2. **Enable Auto-Scaling**: Ensure `auto_scaling_enabled` is set to `true` in `configs/performance_config.yaml`.
3. **Logs**: Review `logs/orchestrator/orchestrator_main.log` to identify if any scaling triggers were ignored.

### 7. Authentication Failures
**Symptoms**: Users cannot log in, or agent authentication is failing.

**Possible Causes**:
- **Expired Tokens**: Tokens issued by the authentication server have expired.
- **Misconfigured Authentication API**: Incorrect configuration in `authentication.py`.

**Solution**:
1. **Refresh Tokens**: Issue new tokens using the endpoint `POST /api/authentication/refresh`.
2. **Update Configuration**: Open `frontend/api/endpoints/authentication.py` and verify authentication settings.
3. **Check Logs**: Check `logs/authentication/auth_access.log` for more detailed errors.

### 8. Model Training Takes Too Long
**Symptoms**: Training sessions are taking longer than expected, causing delays.

**Possible Causes**:
- **Large Model**: The model being used is too complex for the given hardware.
- **Inefficient Data Sharding**: Data sharding may be uneven, resulting in workload imbalance.

**Solution**:
1. **Simplify Model**: Use a smaller or quantized version of the model (`core/models/model_quantization.py`).
2. **Adjust Sharding Strategy**: Use `core/data/data_sharder.py` to ensure that data is evenly distributed across agents.
3. **Logs**: View agent logs (`logs/agents/agent_1.log`) for potential issues during training.

### 9. Dashboard Not Displaying Metrics
**Symptoms**: Metrics are not visible on the Grafana dashboard, or some panels show errors.

**Possible Causes**:
- **Prometheus Configuration Issue**: Prometheus is not scraping the required targets.
- **Incorrect Data Source**: Grafana is not correctly configured to connect to the Prometheus data source.

**Solution**:
1. **Check Prometheus Targets**: Access Prometheus at `http://localhost:9090/targets` to verify that all targets are up.
2. **Update Grafana Data Source**: In Grafana (`http://localhost:3000`), navigate to **Configuration > Data Sources** and verify Prometheus settings.
3. **Logs**: View `logs/system_monitor/communication.log` for detailed network activity information.

## Best Practices for Avoiding Issues
1. **Monitor Logs Regularly**: Set up alerts for critical errors using **Prometheus** or **Grafana** to catch issues early.
2. **Verify Configurations Before Deployment**: Use automated scripts to verify that configurations are consistent across nodes.
3. **Automated Health Checks**: Implement health check endpoints for agents and orchestrators and use Kubernetes liveness and readiness probes to ensure they stay operational.
4. **Resource Allocation Limits**: Define resource allocation limits to avoid overloading nodes, especially during training.

## Summary
The **Troubleshooting Guide** provides comprehensive solutions to common issues encountered in the Decentralized AI System. With detailed steps for log analysis, configuration checks, and resource optimization, users can diagnose and fix problems efficiently, ensuring the system runs smoothly.

For more detailed monitoring and optimization techniques, refer to the [Monitoring Guide](monitoring_guide.md) or [Performance Optimization Guide](performance_optimization.md).