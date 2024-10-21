# Logging Guide

## Overview
Logging is a critical aspect of the **Decentralized AI System** to ensure transparency, traceability, and efficient debugging. This document describes the logging architecture, configurations, and best practices for effectively managing logs in the system. The logging system is implemented to monitor the behavior of various components, ensure security, and assist in troubleshooting issues.

## Logging Architecture
The system uses a **centralized logging directory** where logs are collected from different components, including agents, orchestrators, blockchain nodes, and monitoring services. Each log file serves a specific purpose and is segregated based on the role of the component to facilitate efficient log management.

The key features of the logging architecture are:
- **Centralized Directory**: All logs are stored in the `logs/` directory.
- **Component-specific Logs**: Logs are categorized by component (e.g., agents, orchestrators, blockchain).
- **Structured Logging**: Uses standardized logging formats to allow efficient parsing and analysis.
- **Rotating Logs**: Implements log rotation to avoid disk space issues.
- **Real-time Monitoring**: Logs are integrated with monitoring tools for real-time alerting.

## Log Locations
- **Agents Logs**: Located at `logs/agents/`, e.g., `agent_1.log`, `agent_2.log`. These logs record training activities, resource usage, and interactions with other agents or orchestrators.
- **Orchestrator Logs**: Located at `logs/orchestrator/`, e.g., `orchestrator_main.log`, `backup_orchestrator.log`. These logs provide details of aggregation tasks, agent orchestration, and secure aggregation.
- **Model Registry Logs**: Located at `logs/model_registry/`, these logs keep track of model versioning, registry updates, and version metrics.
- **Blockchain Logs**: Located at `logs/blockchain/`, e.g., `blockchain_node_1.log`. These logs track consensus, agent contributions, and smart contract events.
- **System Monitor Logs**: Located at `logs/system_monitor/`, these logs record system resource usage, communication traces, and error events.
- **Authentication Logs**: Located at `logs/authentication/`, e.g., `auth_access.log`, `token_issue.log`. These logs are used to track authentication and authorization events.

## Logging Configuration
The logging configuration is defined in the `configs/logging_config.yaml` file. This file allows you to configure different log levels, output formats, and file sizes for log rotation.

### Example Logging Configuration (`configs/logging_config.yaml`)
```yaml
logging:
  version: 1
  disable_existing_loggers: false
  formatters:
    standard:
      format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: standard
      stream: ext://sys.stdout
    file:
      class: logging.handlers.RotatingFileHandler
      level: INFO
      formatter: standard
      filename: logs/system_monitor/system_monitor.log
      maxBytes: 10485760  # 10MB
      backupCount: 5
  root:
    level: DEBUG
    handlers: [console, file]
```
- **Formatters**: Define the format of log messages.
- **Handlers**: Specify where logs are sent (e.g., console, file).
- **RotatingFileHandler**: Enables log rotation to manage disk usage.

## Logging Best Practices
1. **Use Appropriate Log Levels**:
   - **DEBUG**: For detailed system behavior and debugging purposes.
   - **INFO**: To log general information such as successful completion of tasks.
   - **WARNING**: To indicate potential issues that are non-critical.
   - **ERROR**: For errors that prevent a specific operation from continuing.
   - **CRITICAL**: For serious errors that might require immediate attention.

2. **Centralized Logging**: Ensure all services log to the central `logs/` directory to facilitate debugging.

3. **Avoid Sensitive Information**: Do not log sensitive data such as user passwords, secrets, or personal information.

4. **Structured Logging**: Always use a consistent format for log entries to facilitate parsing and analysis. Use JSON format if you need to integrate with external log analysis tools.

5. **Monitoring and Alerts**: Integrate logs with **Prometheus** or **Grafana** to create dashboards and configure alerts for critical events.

6. **Log Rotation**: Make sure to configure log rotation to prevent logs from consuming too much disk space.

## Viewing Logs
To view logs, navigate to the relevant log directory and use standard Unix commands such as `cat`, `tail`, or `less`:
```bash
# View the latest entries in the orchestrator log
tail -f logs/orchestrator/orchestrator_main.log
```
You can also use log parsing tools like **grep** to filter logs by level or component:
```bash
# Search for all ERROR messages in the orchestrator log
grep "ERROR" logs/orchestrator/orchestrator_main.log
```

## Integrating Logs with Monitoring Tools
- **Prometheus**: Use Prometheus exporters to collect log-based metrics. Set up alerts to notify administrators of high error rates or other anomalies.
- **Grafana**: Visualize logs using Grafana by connecting it to the Prometheus data source. Dashboards can be created to track important events in real-time.
- **Elastic Stack (ELK)**: You can integrate with the **ELK Stack (Elasticsearch, Logstash, Kibana)** for advanced log analysis, full-text searching, and visualization. Logs can be shipped to Elasticsearch via Logstash for centralized indexing.

## Troubleshooting Using Logs
- **Authentication Issues**: Check `auth_access.log` to identify failed login attempts or unauthorized access.
- **Training Failures**: Review agent logs (e.g., `agent_1.log`) to determine if resource limits or errors caused training interruptions.
- **Blockchain Consensus Errors**: Consult the blockchain logs to identify consensus or smart contract issues.

## Summary
Logging is a fundamental feature of the Decentralized AI System that helps in maintaining transparency, security, and ease of troubleshooting. This guide covers where logs are stored, how they are configured, and best practices to ensure efficient logging. With well-organized logs, users can maintain the health of the system, quickly diagnose problems, and ensure smooth operation of all components.

For more details or troubleshooting specific components, refer to the [Troubleshooting Guide](troubleshooting.md).

