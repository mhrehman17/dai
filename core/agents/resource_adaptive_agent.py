import logging
import threading
from typing import List
from core.agents.distributed_agent import DistributedAgent
from core.utils.resource_manager import ResourceManager
from core.utils.log_utils import LogUtils

class ResourceAdaptiveAgent(DistributedAgent):
    def __init__(self, agent_id: str, server_address: str, peers: List[str],
                 logger: logging.Logger = None, cpu_threshold: float = 75.0, mem_threshold: float = 70.0):
        """
        Initializes a ResourceAdaptiveAgent that adapts its behavior based on resource usage.
        :param agent_id: Unique identifier for the agent.
        :param server_address: gRPC server address to connect to.
        :param peers: List of peer agent identifiers.
        :param logger: Logger instance to log agent operations.
        :param cpu_threshold: CPU usage threshold beyond which adaptations occur.
        :param mem_threshold: Memory usage threshold beyond which adaptations occur.
        """
        super().__init__(agent_id, server_address, peers, logger)
        self.resource_manager = ResourceManager(logger=self.logger)
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold
        self.adaptive_interval = 5  # Interval in seconds for adaptive checks
        self.is_adapting = False

    def start_agent(self):
        """
        Starts the resource adaptive agent, enabling adaptive behavior and communication with peers.
        """
        super().start_agent()
        self.is_adapting = True
        threading.Thread(target=self._adaptive_behavior, daemon=True).start()

    def stop_agent(self):
        """
        Stops the resource adaptive agent.
        """
        self.is_adapting = False
        super().stop_agent()

    def _adaptive_behavior(self):
        """
        Continuously checks resource usage and adapts the agent's behavior accordingly.
        """
        while self.is_adapting:
            # Retrieve resource metrics
            cpu_usage = self.resource_manager.get_cpu_usage()
            memory_usage = self.resource_manager.get_memory_usage()

            # Adapt based on CPU usage
            if cpu_usage > self.cpu_threshold:
                self.logger.warning(f"CPU usage ({cpu_usage}%) exceeded threshold ({self.cpu_threshold}%). Reducing activity.")
                self._reduce_activity()
            else:
                self.logger.info(f"CPU usage ({cpu_usage}%) is within limits.")

            # Adapt based on Memory usage
            if memory_usage > self.mem_threshold:
                self.logger.warning(f"Memory usage ({memory_usage}%) exceeded threshold ({self.mem_threshold}%). Freeing resources.")
                self._free_memory_resources()
            else:
                self.logger.info(f"Memory usage ({memory_usage}%) is within limits.")

            threading.Event().wait(self.adaptive_interval)

    def _reduce_activity(self):
        """
        Reduces the agent's activity to manage high CPU usage.
        """
        # Example logic: reduce the frequency of heartbeat checks or tasks
        if self.heartbeat_interval < 10:
            self.heartbeat_interval += 1
            self.logger.info(f"Heartbeat interval increased to {self.heartbeat_interval} seconds to reduce CPU load.")

    def _free_memory_resources(self):
        """
        Frees memory resources to manage high memory usage.
        """
        # Example logic: stop non-critical tasks or clear caches
        self.logger.info("Freeing non-critical memory resources.")
        # Here you could add logic to clear caches or pause non-essential computations

# Example usage
if __name__ == "__main__":
    # Set up logger
    adaptive_logger = LogUtils.setup_logger(name="resource_adaptive_agent", level=logging.INFO)

    # Initialize and start a resource adaptive agent
    resource_adaptive_agent = ResourceAdaptiveAgent(
        agent_id="adaptive_agent_1",
        server_address="localhost:50051",
        peers=["peer_1", "peer_2"],
        logger=adaptive_logger,
        cpu_threshold=75.0,
        mem_threshold=70.0
    )
    resource_adaptive_agent.start_agent()

    # Allow agent to run for a while
    try:
        threading.Event().wait(20)
    finally:
        resource_adaptive_agent.stop_agent()
