import time
from core.ledger.blockchain import Blockchain
from core.ledger.node_setup.node_init import NodeInitializer
from threading import Thread

class MinerNode(NodeInitializer):
    def __init__(self, node_id: str, peers: list, data_dir: str = "./node_data", mining_interval: int = 5):
        """
        Initializes a miner node with mining capabilities.
        :param node_id: Unique identifier for the node.
        :param peers: List of peer node identifiers.
        :param data_dir: Directory to store blockchain data.
        :param mining_interval: Interval in seconds between mining attempts.
        """
        super().__init__(node_id, peers, data_dir)
        self.mining_interval = mining_interval
        self.mining_thread = Thread(target=self.mine)
        self.is_mining = False

    def start_mining(self):
        """
        Starts the mining process in a separate thread.
        """
        self.is_mining = True
        if not self.mining_thread.is_alive():
            self.mining_thread = Thread(target=self.mine)
            self.mining_thread.start()
        print(f"Mining started for node {self.node_id}.")

    def stop_mining(self):
        """
        Stops the mining process.
        """
        self.is_mining = False
        self.mining_thread.join()
        print(f"Mining stopped for node {self.node_id}.")

    def mine(self):
        """
        Continuously mines new blocks at a specified interval.
        """
        while self.is_mining:
            time.sleep(self.mining_interval)
            self.mine_new_block()

    def mine_new_block(self):
        """
        Mines a new block and adds it to the blockchain.
        """
        data = f"Mined by {self.node_id} at {time.time()}"
        self.blockchain.add_block(data)
        self.save_blockchain_state()
        print(f"New block mined and added by {self.node_id}: {self.blockchain.get_last_block().hash}")

# Example usage
if __name__ == "__main__":
    # Initialize miner node with some peers
    miner_node = MinerNode(node_id="miner1", peers=["node2", "node3"], mining_interval=3)
    miner_node.start_mining()

    # Allow mining for some time
    try:
        time.sleep(15)  # Simulate mining time
    finally:
        miner_node.stop_mining()

    # Print the blockchain
    for block in miner_node.blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Data: {block.data}")
