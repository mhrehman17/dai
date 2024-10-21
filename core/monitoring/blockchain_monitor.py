import logging
import time
import threading
from typing import List, Tuple
import requests


class BlockchainMonitor:
    def __init__(self, nodes: List[Tuple[str, int]], polling_interval: int = 10, logger: logging.Logger = None):
        """
        Initializes the BlockchainMonitor for monitoring blockchain node status and metrics.
        :param nodes: A list of node addresses in the format (host, port).
        :param polling_interval: The time interval (in seconds) between polling each node.
        :param logger: Logger instance to log monitoring activities.
        """
        self.nodes = nodes
        self.polling_interval = polling_interval
        self.logger = logger or logging.getLogger(__name__)
        self._stop_event = threading.Event()  # Thread-safe stop control
        self.monitor_thread = None

    def start_monitoring(self):
        """
        Starts monitoring blockchain nodes in a separate thread.
        """
        if self.monitor_thread is None or not self.monitor_thread.is_alive():
            self._stop_event.clear()
            self.monitor_thread = threading.Thread(target=self._monitor_nodes, daemon=True)
            self.monitor_thread.start()
            self.logger.info("Blockchain monitoring started.")

    def stop_monitoring(self):
        """
        Stops monitoring blockchain nodes.
        """
        if self.monitor_thread and self.monitor_thread.is_alive():
            self._stop_event.set()
            self.monitor_thread.join()  # Ensure the monitoring thread is joined
            self.logger.info("Blockchain monitoring stopped.")

    def _monitor_nodes(self):
        """
        Monitors the blockchain nodes by sending periodic requests and logging their status.
        Implements retry logic for better handling of transient failures.
        """
        while not self._stop_event.is_set():
            for host, port in self.nodes:
                node_url = f"http://{host}:{port}/status"
                retry_count = 0
                max_retries = 3
                while retry_count < max_retries and not self._stop_event.is_set():
                    try:
                        response = requests.get(node_url, timeout=5)
                        if response.status_code == 200:
                            self.logger.info(f"Node at {host}:{port} is active. Status: {response.json()}")
                            break  # Exit retry loop on success
                        else:
                            self.logger.warning(f"Node at {host}:{port} responded with status code {response.status_code}")
                            break  # No need to retry if node responds with a non-200 status
                    except requests.exceptions.RequestException as e:
                        retry_count += 1
                        self.logger.error(
                            f"Failed to reach node at {host}:{port} on attempt {retry_count}: {e}"
                        )
                        if retry_count == max_retries:
                            self.logger.error(f"Max retries reached for node {host}:{port}. Giving up.")
                    time.sleep(1)  # Small delay before retrying
            time.sleep(self.polling_interval)

    def log_node_metrics(self, metrics_endpoint: str):
        """
        Logs detailed metrics for each node by querying the specified metrics endpoint.
        :param metrics_endpoint: Endpoint to access node metrics, typically '/metrics'.
        """
        for host, port in self.nodes:
            try:
                url = f"http://{host}:{port}{metrics_endpoint}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    self.logger.info(f"Metrics for node at {host}:{port}: {response.text}")
                else:
                    self.logger.warning(f"Failed to get metrics for node at {host}:{port}, status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to get metrics from node at {host}:{port}: {e}")


# Example usage
if __name__ == "__main__":
    # Set up logger
    blockchain_logger = logging.getLogger("blockchain_monitor")
    blockchain_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    blockchain_logger.addHandler(console_handler)

    # Initialize BlockchainMonitor
    blockchain_monitor = BlockchainMonitor(
        nodes=[("localhost", 8545), ("localhost", 8546)],
        polling_interval=15,
        logger=blockchain_logger
    )
    
    # Start monitoring blockchain nodes
    blockchain_monitor.start_monitoring()

    # Allow some time for demonstration purposes
    try:
        time.sleep(60)  # Keep running for 1 minute to simulate monitoring
    finally:
        blockchain_monitor.stop_monitoring()
