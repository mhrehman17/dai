import logging
import threading
import random
from core.utils.resource_manager import ResourceManager
from core.communication.grpc_client import BlockchainClient
from core.utils.metric_utils import MetricUtils
from core.utils.log_utils import LogUtils
from typing import List
import time

class DistributedAgent:
    def __init__(self, agent_id: str, server_address: str, peers: List[str], 
                 logger: logging.Logger = None):
        """
        Initializes a distributed agent to manage communication and processing in a decentralized network.
        :param agent_id: Unique identifier for the agent.
        :param server_address: gRPC server address to connect to.
        :param peers: List of peer agent identifiers.
        :param logger: Logger instance to log agent operations.
        """
        self.agent_id = agent_id
        self.server_address = server_address
        self.peers = peers
        self.logger = logger or logging.getLogger(__name__)
        self.resource_manager = ResourceManager(logger=self.logger)
        self.blockchain_client = BlockchainClient(server_address=server_address)
        self.metric_utils = MetricUtils(logger=self.logger)
        self.heartbeat_interval = 5  # Interval in seconds for heartbeat
        self.is_active = False
        self.iteration_limit = 20  # Limiting iterations for testing purposes
        self.current_iteration = 0
        self.failed_heartbeats = {peer: 0 for peer in self.peers}  # Track failed heartbeats per peer

    def start_agent(self):
        """
        Starts the distributed agent, enabling communication with peers and handling tasks.
        """
        self.is_active = True
        self.logger.info(f"Agent {self.agent_id} started.")
        threading.Thread(target=self._heartbeat, daemon=True).start()
        threading.Thread(target=self._monitor_resources, daemon=True).start()

    def stop_agent(self):
        """
        Stops the distributed agent.
        """
        self.is_active = False
        self.logger.info(f"Agent {self.agent_id} stopped.")

    def _heartbeat(self):
        """
        Sends a heartbeat signal to peers at regular intervals.
        """
        while self.is_active and self.current_iteration < self.iteration_limit:
            self.logger.info(f"Agent {self.agent_id} sending heartbeat to peers: {self.peers}")
            # Simulate peer-to-peer heartbeat communication
            for peer in self.peers:
                success = random.choices([True, False], weights=[0.8, 0.2], k=1)[0]  # Higher success rate

                if success:
                    self.logger.info(f"Heartbeat successfully sent to peer {peer}")
                    self.failed_heartbeats[peer] = 0  # Reset failure count on success
                else:
                    self.failed_heartbeats[peer] += 1

                    # Only log a warning if the peer has failed consecutively more than 2 times
                    if self.failed_heartbeats[peer] > 2:
                        self.logger.warning(
                            f"Failed to send heartbeat to peer {peer} "
                            f"(consecutive failures: {self.failed_heartbeats[peer]})"
                        )

            self.current_iteration += 1
            if self.current_iteration >= self.iteration_limit:
                self.logger.info(f"Agent {self.agent_id} reached iteration limit, stopping heartbeat.")
                self.stop_agent()

            time.sleep(self.heartbeat_interval)

    def _monitor_resources(self):
        """
        Monitors system resources and logs the metrics.
        """
        while self.is_active and self.current_iteration < self.iteration_limit:
            cpu_usage = self.resource_manager.get_cpu_usage()
            memory_usage = self.resource_manager.get_memory_usage()

            # Log resource usage
            self.metric_utils.log_metric("CPU Usage", cpu_usage)
            self.metric_utils.log_metric("Memory Usage", memory_usage)

            self.current_iteration += 1
            if self.current_iteration >= self.iteration_limit:
                self.logger.info(f"Agent {self.agent_id} reached iteration limit, stopping resource monitoring.")
                self.stop_agent()

            time.sleep(self.heartbeat_interval)

    def request_blockchain_state(self):
        """
        Requests the current blockchain state from the server.
        """
        blockchain_state = self.blockchain_client.get_blockchain_state()
        if blockchain_state:
            self.logger.info(f"Agent {self.agent_id} retrieved blockchain state.")
            return blockchain_state
        else:
            self.logger.error(f"Agent {self.agent_id} failed to retrieve blockchain state.")
            return None

    def add_data_to_blockchain(self, data: str):
        """
        Requests the server to add a new block with the provided data.
        :param data: Data to add to the blockchain.
        """
        self.blockchain_client.add_block(data=data)
        self.logger.info(f"Agent {self.agent_id} requested to add data to blockchain: {data}")

# Example usage
if __name__ == "__main__":
    # Set up logger
    agent_logger = LogUtils.setup_logger(name="distributed_agent", level=logging.INFO)

    # Initialize and start a distributed agent
    distributed_agent = DistributedAgent(
        agent_id="agent_1",
        server_address="localhost:50051",
        peers=["peer_1", "peer_2"],
        logger=agent_logger
    )
    distributed_agent.start_agent()

    # Allow agent to run for a while
    try:
        threading.Event().wait(15)
    finally:
        distributed_agent.stop_agent()
