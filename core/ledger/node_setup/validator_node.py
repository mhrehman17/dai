from core.ledger.blockchain import Blockchain
from core.ledger.node_setup.node_init import NodeInitializer
from core.ledger.consensus_mechanism import ConsensusMechanism
from threading import Thread
import time
from typing import List

class ValidatorNode(NodeInitializer):
    def __init__(self, node_id: str, peers: List[str], data_dir: str = "./node_data", validation_interval: int = 5):
        """
        Initializes a validator node with validation capabilities.
        :param node_id: Unique identifier for the node.
        :param peers: List of peer node identifiers.
        :param data_dir: Directory to store blockchain data.
        :param validation_interval: Interval in seconds between validation checks.
        """
        super().__init__(node_id, peers, data_dir)
        self.validation_interval = validation_interval
        self.validation_thread = Thread(target=self.validate_chain)
        self.is_validating = False

    def start_validation(self):
        """
        Starts the validation process in a separate thread.
        """
        self.is_validating = True
        if not self.validation_thread.is_alive():
            self.validation_thread = Thread(target=self.validate_chain)
            self.validation_thread.start()
        print(f"Validation started for node {self.node_id}.")

    def stop_validation(self):
        """
        Stops the validation process.
        """
        self.is_validating = False
        self.validation_thread.join()
        print(f"Validation stopped for node {self.node_id}.")

    def validate_chain(self):
        """
        Continuously validates the blockchain at a specified interval.
        """
        while self.is_validating:
            time.sleep(self.validation_interval)
            is_valid = self.blockchain.is_chain_valid()
            if is_valid:
                print(f"Node {self.node_id}: Blockchain is valid.")
            else:
                print(f"Node {self.node_id}: Blockchain is invalid. Initiating consensus.")
                self.initiate_consensus_with_peers()

    def initiate_consensus_with_peers(self):
        """
        Gathers blockchain data from peers and initiates a consensus mechanism to resolve discrepancies.
        """
        peer_blockchains = self.get_peer_blockchains()
        self.initiate_consensus(peer_blockchains)

    def get_peer_blockchains(self) -> List[Blockchain]:
        """
        Simulates fetching blockchain data from peer nodes.
        :return: A list of blockchain instances from peer nodes.
        """
        peer_blockchains = []
        for peer_id in self.peers:
            # In a real-world scenario, this would be replaced by network requests to get peer blockchain states.
            peer_blockchain = Blockchain()
            peer_blockchain.add_block(f"Block from {peer_id} - Simulated for consensus")
            peer_blockchains.append(peer_blockchain)
        return peer_blockchains

# Example usage
if __name__ == "__main__":
    # Initialize validator node with some peers
    validator_node = ValidatorNode(node_id="validator1", peers=["miner1", "node2"], validation_interval=3)
    validator_node.start_validation()

    # Allow validation for some time
    try:
        time.sleep(15)  # Simulate validation time
    finally:
        validator_node.stop_validation()

    # Print the blockchain
    for block in validator_node.blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Data: {block.data}")
