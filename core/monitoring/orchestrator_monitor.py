import logging
import requests
import threading
import time
from typing import List, Tuple

class OrchestratorMonitor:
    def __init__(self, orchestrator_nodes: List[Tuple[str, int]], polling_interval: int = 10, logger: logging.Logger = None):
        """
        Initializes the OrchestratorMonitor for monitoring orchestrator node status and metrics.
        :param orchestrator_nodes: A list of orchestrator node addresses in the format (host, port).
        :param polling_interval: The time interval (in seconds) between polling each node.
        :param logger: Logger instance to log monitoring activities.
        """
        self.orchestrator_nodes = orchestrator_nodes
        self.polling_interval = polling_interval
        self.logger = logger or logging.getLogger(__name__)
        self.running = False

    def start_monitoring(self):
        """
        Starts monitoring orchestrator nodes in a separate thread.
        """
        self.running = True
        threading.Thread(target=self._monitor_nodes, daemon=True).start()
        self.logger.info("Orchestrator monitoring started.")

    def stop_monitoring(self):
        """
        Stops monitoring orchestrator nodes.
        """
        self.running = False
        self.logger.info("Orchestrator monitoring stopped.")

    def _monitor_nodes(self):
        """
        Monitors the orchestrator nodes by sending periodic requests and logging their status.
        """
        while self.running:
            for host, port in self.orchestrator_nodes:
                try:
                    url = f"http://{host}:{port}/orchestrator_status"
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        status_info = response.json()
                        self.logger.info(f"Orchestrator at {host}:{port} is active. Status: {status_info}")
                    else:
                        self.logger.warning(f"Orchestrator at {host}:{port} responded with status code {response.status_code}")
                except requests.exceptions.RequestException as e:
                    self.logger.error(f"Failed to reach orchestrator at {host}:{port}: {e}")
            time.sleep(self.polling_interval)

    def log_node_metrics(self, metrics_endpoint: str = '/orchestrator_metrics'):
        """
        Logs detailed metrics for each orchestrator node by querying the specified metrics endpoint.
        :param metrics_endpoint: Endpoint to access orchestrator metrics.
        """
        for host, port in self.orchestrator_nodes:
            try:
                url = f"http://{host}:{port}{metrics_endpoint}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.logger.info(f"Metrics for orchestrator at {host}:{port}: {response.text}")
                else:
                    self.logger.warning(f"Failed to get metrics for orchestrator at {host}:{port}, status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to get metrics from orchestrator at {host}:{port}: {e}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    orchestrator_logger = logging.getLogger("orchestrator_monitor")
    orchestrator_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    orchestrator_logger.addHandler(console_handler)

    # Initialize OrchestratorMonitor
    orchestrator_monitor = OrchestratorMonitor(
        orchestrator_nodes=[("localhost", 8080), ("localhost", 8081)],
        polling_interval=15,
        logger=orchestrator_logger
    )
    
    # Start monitoring orchestrator nodes
    orchestrator_monitor.start_monitoring()

    # Allow some time for monitoring demonstration purposes
    try:
        time.sleep(60)  # Keep running for 1 minute to simulate monitoring
    finally:
        orchestrator_monitor.stop_monitoring()
