import logging
import time
import requests
import threading
from typing import List, Tuple, Optional

class PrometheusMonitor:
    def __init__(self, prometheus_endpoints: List[Tuple[str, int]], polling_interval: int = 10, logger: Optional[logging.Logger] = None):
        """
        Initializes the PrometheusMonitor for monitoring metrics collected via Prometheus endpoints.
        :param prometheus_endpoints: A list of Prometheus server addresses in the format (host, port).
        :param polling_interval: The time interval (in seconds) between polling each endpoint.
        :param logger: Logger instance to log monitoring activities.
        """
        self.prometheus_endpoints = prometheus_endpoints
        self.polling_interval = polling_interval
        self.logger = logger or logging.getLogger(__name__)
        self.running = False

    def start_monitoring(self):
        """
        Starts monitoring Prometheus metrics in a separate thread.
        """
        self.running = True
        threading.Thread(target=self._monitor_metrics, daemon=True).start()
        self.logger.info("Prometheus monitoring started.")

    def stop_monitoring(self):
        """
        Stops monitoring Prometheus metrics.
        """
        self.running = False
        self.logger.info("Prometheus monitoring stopped.")

    def _monitor_metrics(self):
        """
        Monitors metrics collected by Prometheus by sending periodic requests to Prometheus servers.
        """
        while self.running:
            for host, port in self.prometheus_endpoints:
                try:
                    url = f"http://{host}:{port}/api/v1/query?query=up"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        metrics = response.json()
                        self.logger.info(f"Metrics from Prometheus at {host}:{port}: {metrics}")
                    else:
                        self.logger.warning(f"Failed to get metrics from Prometheus at {host}:{port}, status code {response.status_code}")
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Failed to reach Prometheus at {host}:{port}: {e}")
            time.sleep(self.polling_interval)

    def log_custom_query(self, query: str):
        """
        Logs metrics from Prometheus based on a custom query.
        :param query: The Prometheus query to execute.
        """
        for host, port in self.prometheus_endpoints:
            try:
                url = f"http://{host}:{port}/api/v1/query?query={query}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    metrics = response.json()
                    self.logger.info(f"Custom query metrics from Prometheus at {host}:{port}: {metrics}")
                else:
                    self.logger.warning(f"Failed to execute custom query on Prometheus at {host}:{port}, status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to execute custom query on Prometheus at {host}:{port}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    prometheus_logger = logging.getLogger("prometheus_monitor")
    prometheus_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    prometheus_logger.addHandler(console_handler)

    # Initialize PrometheusMonitor
    prometheus_endpoints_info = [
        ("localhost", 9090),
        ("localhost", 9091)
    ]
    prometheus_monitor = PrometheusMonitor(prometheus_endpoints=prometheus_endpoints_info, polling_interval=15, logger=prometheus_logger)

    # Start monitoring Prometheus metrics
    prometheus_monitor.start_monitoring()

    # Allow some time for demonstration purposes
    try:
        time.sleep(60)  # Keep running for 1 minute to simulate monitoring
    finally:
        prometheus_monitor.stop_monitoring()
