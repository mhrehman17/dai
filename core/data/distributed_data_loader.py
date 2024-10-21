import os
import logging
import threading
from typing import List, Tuple, Any
from core.data.data_cache import DataCache
from core.communication.p2p_network import P2PNetwork
from core.utils.log_utils import LogUtils

class DistributedDataLoader:
    def __init__(self, host: str, port: int, peers: List[Tuple[str, int]],
                 cache_dir: str = './data_cache', logger: logging.Logger = None):
        """
        Initializes a DistributedDataLoader that shares data between peers in a P2P network.
        :param host: The hostname or IP address to bind the server.
        :param port: The port on which the server will listen.
        :param peers: A list of peer addresses in the format (host, port).
        :param cache_dir: Directory where cached data should be stored.
        :param logger: Logger instance to log distributed data loader activities.
        """
        self.logger = logger or logging.getLogger(__name__)
        self.p2p_network = P2PNetwork(host, port, peers, logger=self.logger)
        self.data_cache = DataCache(cache_dir=cache_dir, logger=self.logger)
        self.running = False

    def start_loader(self):
        """
        Starts the distributed data loader.
        """
        self.running = True
        self.p2p_network.start_network()
        threading.Thread(target=self._receive_data, daemon=True).start()
        self.logger.info("Distributed data loader started.")

    def stop_loader(self):
        """
        Stops the distributed data loader.
        """
        self.running = False
        self.p2p_network.stop_network()
        self.logger.info("Distributed data loader stopped.")

    def _receive_data(self):
        """
        Continuously listens for data from peers and caches it locally.
        """
        while self.running:
            # This method simulates the reception of data and caching it
            for peer in self.p2p_network.peers:
                message = self.p2p_network.send_message_to_peer(peer, "REQUEST_DATA")
                if message:
                    cache_key = self.data_cache._generate_cache_key(message)
                    self.data_cache.save_to_cache(cache_key, message)
                    self.logger.info(f"Data received and cached from peer {peer}")

    def distribute_data(self, data: Any):
        """
        Distributes data to all connected peers in the network.
        :param data: The data to distribute.
        """
        cache_key = self.data_cache._generate_cache_key(data)
        self.data_cache.save_to_cache(cache_key, data)
        self.logger.info(f"Data cached locally with key: {cache_key}")
        
        for peer in self.p2p_network.peers:
            self.p2p_network.send_message_to_peer(peer, data)
            self.logger.info(f"Data sent to peer {peer}")

    def load_cached_data(self, key: str) -> Any:
        """
        Loads data from the local cache if available.
        :param key: The unique identifier for the cached data.
        :return: The cached data, or None if not found.
        """
        return self.data_cache.load_from_cache(key)

# Example usage
if __name__ == "__main__":
    # Set up logger
    data_loader_logger = LogUtils.setup_logger(name="distributed_data_loader", level=logging.INFO)

    # Initialize and start a distributed data loader
    distributed_data_loader = DistributedDataLoader(
        host="localhost",
        port=6000,
        peers=[("localhost", 6001)],
        logger=data_loader_logger
    )
    distributed_data_loader.start_loader()

    # Example: Distribute data to peers
    data = {"sample": "This is some distributed data", "number": 123}
    distributed_data_loader.distribute_data(data)

    # Allow some time for demonstration purposes
    try:
        threading.Event().wait(10)
    finally:
        distributed_data_loader.stop_loader()