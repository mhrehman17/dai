import logging
import time
import psutil
import threading
from typing import List, Dict, Optional

class PerformanceAnalyzer:
    def __init__(self, nodes: List[Dict[str, str]], polling_interval: int = 10, logger: Optional[logging.Logger] = None):
        """
        Initializes the PerformanceAnalyzer for monitoring system performance metrics.
        :param nodes: A list of nodes to be analyzed, containing information such as host and identifier.
        :param polling_interval: The time interval (in seconds) between polling each node.
        :param logger: Logger instance to log performance metrics.
        """
        self.nodes = nodes
        self.polling_interval = polling_interval
        self.logger = logger or logging.getLogger(__name__)
        self.running = False

    def start_monitoring(self):
        """
        Starts monitoring system performance metrics in a separate thread.
        """
        self.running = True
        threading.Thread(target=self._monitor_performance, daemon=True).start()
        self.logger.info("Performance monitoring started.")

    def stop_monitoring(self):
        """
        Stops monitoring system performance metrics.
        """
        self.running = False
        self.logger.info("Performance monitoring stopped.")

    def _monitor_performance(self):
        """
        Monitors CPU, memory, and disk utilization and logs the data periodically.
        """
        while self.running:
            try:
                # Capture system metrics
                cpu_usage = psutil.cpu_percent(interval=1)
                memory_info = psutil.virtual_memory()
                disk_usage = psutil.disk_usage('/')

                # Log CPU, Memory, and Disk metrics
                self.logger.info(f"CPU Usage: {cpu_usage}%")
                self.logger.info(f"Memory Usage: {memory_info.percent}%")
                self.logger.info(f"Disk Usage: {disk_usage.percent}%")

                # Optionally, you can store these metrics in a file or a database for later analysis.

                time.sleep(self.polling_interval - 1)  # Adjust sleep to maintain consistent polling intervals
            except Exception as e:
                self.logger.error(f"Error while monitoring performance: {e}")
                time.sleep(self.polling_interval)

    def log_node_performance(self, node_id: str, custom_metrics: Dict[str, float]):
        """
        Logs the performance metrics for a specific node based on custom metrics.
        :param node_id: Unique identifier for the node.
        :param custom_metrics: A dictionary of performance metrics to be logged.
        """
        for metric, value in custom_metrics.items():
            self.logger.info(f"Node {node_id} - {metric}: {value}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    performance_logger = logging.getLogger("performance_analyzer")
    performance_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    performance_logger.addHandler(console_handler)

    # Initialize PerformanceAnalyzer
    nodes_info = [
        {"host": "localhost", "id": "node_1"},
        {"host": "localhost", "id": "node_2"}
    ]
    performance_analyzer = PerformanceAnalyzer(nodes=nodes_info, polling_interval=15, logger=performance_logger)

    # Start monitoring system performance
    performance_analyzer.start_monitoring()

    # Allow some time for demonstration purposes
    try:
        time.sleep(60)  # Keep running for 1 minute to simulate monitoring
    finally:
        performance_analyzer.stop_monitoring()
