import logging
import threading
import time
from typing import List, Dict, Optional

class AdaptiveOrchestrator:
    def __init__(self, nodes: List[Dict[str, str]], polling_interval: int = 10, logger: Optional[logging.Logger] = None):
        """
        Initializes the AdaptiveOrchestrator for managing and orchestrating distributed nodes adaptively.
        :param nodes: A list of nodes containing information such as host and identifier.
        :param polling_interval: The time interval (in seconds) between polling each node for resource availability.
        :param logger: Logger instance to log orchestrating activities.
        """
        self.nodes = nodes
        self.polling_interval = polling_interval
        self.logger = logger or logging.getLogger(__name__)
        self.running = False
        self.node_metrics = {node['id']: {} for node in nodes}

    def start_orchestrating(self):
        """
        Starts orchestrating the distributed nodes in a separate thread.
        """
        self.running = True
        threading.Thread(target=self._orchestrate_nodes, daemon=True).start()
        self.logger.info("Adaptive orchestrating started.")

    def stop_orchestrating(self):
        """
        Stops orchestrating the distributed nodes.
        """
        self.running = False
        self.logger.info("Adaptive orchestrating stopped.")

    def _orchestrate_nodes(self):
        """
        Orchestrates the distributed nodes by polling their status and assigning tasks based on resource availability.
        """
        while self.running:
            try:
                for node in self.nodes:
                    node_id = node.get("id")
                    resource_info = self._fetch_node_resources(node)
                    self.node_metrics[node_id] = resource_info
                    self.logger.info(f"Node {node_id} Resources: {resource_info}")

                # Adaptive task assignment logic
                self._assign_tasks_adaptively()
                time.sleep(self.polling_interval)
            except Exception as e:
                self.logger.error(f"Error while orchestrating nodes: {e}")
                time.sleep(self.polling_interval)

    def _fetch_node_resources(self, node: Dict[str, str]) -> Dict[str, str]:
        """
        Simulates the retrieval of node resource availability metrics.
        :param node: The node to retrieve resource information from.
        :return: A dictionary containing resource information.
        """
        # Simulating resource metric retrieval. In a real implementation, this would involve querying an endpoint.
        return {
            "cpu_usage": "25%",
            "memory_available": "2GB",
            "network_bandwidth": "10Mbps"
        }

    def _assign_tasks_adaptively(self):
        """
        Assigns tasks to nodes adaptively based on their resource availability.
        """
        for node_id, metrics in self.node_metrics.items():
            # Simulated decision-making based on available metrics
            if metrics.get("cpu_usage") and int(metrics["cpu_usage"].strip('%')) < 50:
                self.logger.info(f"Assigning task to node {node_id} due to low CPU usage.")
            else:
                self.logger.info(f"Node {node_id} is overloaded, skipping task assignment.")

# Example usage
if __name__ == "__main__":
    # Set up logger
    orchestrator_logger = logging.getLogger("adaptive_orchestrator")
    orchestrator_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    orchestrator_logger.addHandler(console_handler)

    # Initialize AdaptiveOrchestrator
    nodes_info = [
        {"host": "localhost", "id": "node_1"},
        {"host": "localhost", "id": "node_2"},
        {"host": "localhost", "id": "node_3"}
    ]
    adaptive_orchestrator = AdaptiveOrchestrator(nodes=nodes_info, polling_interval=15, logger=orchestrator_logger)

    # Start orchestrating nodes
    adaptive_orchestrator.start_orchestrating()

    # Allow some time for demonstration purposes
    try:
        time.sleep(60)  # Keep running for 1 minute to simulate orchestration
    finally:
        adaptive_orchestrator.stop_orchestrating()