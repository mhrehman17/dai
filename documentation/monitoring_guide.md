# Monitoring Guide

## Overview
Monitoring is essential to ensure the health, performance, and reliability of the **Decentralized AI System**. This guide explains how to set up monitoring for different components of the system, including agents, orchestrators, blockchain nodes, and edge devices. The monitoring framework uses **Prometheus** and **Grafana** for real-time metrics collection and visualization, alongside other tools for log management and alerting.

## Key Monitoring Tools
- **Prometheus**: Used for metrics collection from various components. Agents and orchestrators are instrumented to expose metrics, which Prometheus scrapes regularly.
- **Grafana**: Provides interactive dashboards for visualizing the metrics collected by Prometheus. It can also be used for alerting based on custom thresholds.
- **Log Collector**: Centralized logging using custom scripts that aggregate logs from agents, orchestrators, and blockchain nodes.
- **Node Exporter**: Provides hardware and OS-level metrics, ensuring proper resource allocation across agents and orchestrators.

## Monitoring Architecture
The **Monitoring System** collects both system-level and component-level metrics from different nodes within the decentralized architecture. Below are the main parts of the monitoring setup:

1. **Prometheus Metrics Exporter**: Agents, orchestrators, and blockchain nodes are instrumented with metrics exporters.
2. **Grafana Dashboard**: Provides a user-friendly view of collected metrics, performance, alerts, and analysis.
3. **Alert Manager**: Alerts are configured based on key metrics such as CPU utilization, memory usage, latency, and training convergence rate.
4. **Log Monitoring**: Logs are aggregated and filtered for critical errors, exceptions, or any unusual activity.

## Setting Up Monitoring

### Step 1: Setting Up Prometheus
#### 1.1. Installation
To install Prometheus, use the following command:
```bash
sudo apt-get update && sudo apt-get install prometheus
```
For Docker users, Prometheus can be run using Docker Compose:
```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

#### 1.2. Configuring Prometheus
The `prometheus.yml` configuration file needs to be updated to scrape metrics from different components:
```yaml
scrape_configs:
  - job_name: 'orchestrator'
    static_configs:
      - targets: ['orchestrator:8001']
  - job_name: 'agent'
    static_configs:
      - targets: ['agent1:8002', 'agent2:8003']
  - job_name: 'blockchain'
    static_configs:
      - targets: ['blockchain_node_1:8004']
```
This configuration sets up Prometheus to collect metrics from the orchestrator, agents, and blockchain nodes.

### Step 2: Setting Up Grafana
#### 2.1. Installation
To install Grafana, use the following commands:
```bash
sudo apt-get install -y adduser libfontconfig1
wget https://dl.grafana.com/oss/release/grafana_8.0.6_amd64.deb
sudo dpkg -i grafana_8.0.6_amd64.deb
```
Alternatively, you can run Grafana using Docker Compose:
```yaml
services:
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    volumes:
      - ./grafana:/var/lib/grafana
```

#### 2.2. Setting Up Dashboards
- Start Grafana by accessing `http://localhost:3000`.
- Log in with the default credentials (`admin` / `admin`).
- Add Prometheus as a data source using the Prometheus server URL (`http://prometheus:9090`).
- Import the pre-configured dashboard JSON files from `core/monitoring/dashboard/` to visualize system metrics.

### Step 3: Setting Up Node Exporter
Node Exporter helps in collecting system-level metrics like CPU, memory, and disk usage.
#### 3.1. Installation
```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.0.1/node_exporter-1.0.1.linux-amd64.tar.gz
tar xvfz node_exporter-1.0.1.linux-amd64.tar.gz
./node_exporter
```
#### 3.2. Configuring Prometheus for Node Exporter
Add Node Exporter targets to `prometheus.yml`:
```yaml
  - job_name: 'node_exporter'
    static_configs:
      - targets: ['localhost:9100']
```

### Step 4: Log Collection and Analysis
Logs are crucial for debugging and identifying the root cause of failures.
#### 4.1. Centralized Log Collection
The `log_collector.py` script in the `core/monitoring/` directory is used to aggregate logs from all agents, orchestrators, and blockchain nodes. Use the following command to start the log collector:
```bash
python core/monitoring/log_collector.py
```
- Logs are saved to the `logs/` directory and categorized by service (e.g., agent, orchestrator).

#### 4.2. Visualizing Logs with ELK Stack (Optional)
- Install **Elasticsearch**, **Logstash**, and **Kibana** for advanced log aggregation, searching, and visualization.
- Configure Logstash to read logs from `logs/` directory and send data to Elasticsearch.
- Use Kibana to visualize the logs and identify errors in real-time.

## Configuring Alerts
### Prometheus Alertmanager
Alerts are configured in the `alert_rules.yml` file to trigger notifications based on specific thresholds.
#### Example Alert Configuration
```yaml
alert_rules:
  groups:
    - name: SystemAlerts
      rules:
        - alert: HighMemoryUsage
          expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 20
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "Memory usage is above 80%"
            description: "Memory usage is critically high on {{ $labels.instance }}"
```
- Alerts for high CPU usage, high memory usage, and agent disconnections can be added in a similar manner.

### Grafana Alerts
Alerts can also be configured directly in Grafana:
- Navigate to a panel that shows metrics.
- Click on the **Alert** tab and configure alert thresholds.
- Set up notifications to be sent via **email**, **Slack**, or other channels when thresholds are crossed.

## Viewing Metrics and Logs
### Grafana Dashboards
- Access **Grafana** at `http://localhost:3000` to view metrics.
- Use pre-configured dashboards to view orchestrator, agent, and blockchain node performance metrics.
- Set time ranges and use filters to drill down into specific time periods and events.

### Using Command Line Tools
- **View Logs**: To check logs for specific services, use the command:
  ```bash
  tail -f logs/orchestrator/orchestrator_main.log
  ```
- **Check System Metrics**: Use `top` or `htop` to see real-time system metrics.
- **Prometheus Console**: Access the Prometheus console at `http://localhost:9090` to query metrics directly.

## Best Practices for Monitoring
1. **Define Meaningful Alerts**: Set alerts for conditions that require action (e.g., high memory, low disk space).
2. **Use Dashboards for Visibility**: Grafana dashboards provide insights into the overall health and performance of the system.
3. **Centralized Log Management**: Ensure all services write logs to a centralized location and consider using **Elasticsearch** and **Kibana** for ease of management.
4. **Automated Metrics Scraping**: Use **Kubernetes** to automate metrics scraping from all services in a cloud deployment.

## Summary
The **Monitoring Guide** provides detailed steps to set up Prometheus, Grafana, and centralized log collection to ensure the health and reliability of the Decentralized AI System. With real-time metrics, alerting, and centralized log management, the system is built to provide transparency and facilitate quick responses to any issues that may arise.

For further details or troubleshooting monitoring setup, refer to the [Troubleshooting Guide](troubleshooting.md).

