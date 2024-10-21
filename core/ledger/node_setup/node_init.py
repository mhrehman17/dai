import os
import json
from core.ledger.blockchain import Blockchain  # Import Blockchain class
from core.ledger.block import Block  # Import Block class
from core.ledger.consensus_mechanism import ConsensusMechanism
from typing import List

class NodeInitializer:
    def __init__(self, node_id: str, peers: List[str], data_dir: str = "./node_data"):
        """
        Initializes a blockchain node with given parameters.
        :param node_id: Unique identifier for the node.
        :param peers: List of peer node identifiers.
        :param data_dir: Directory to store blockchain data.
        """
        self.node_id = node_id
        self.peers = peers
        self.data_dir = data_dir
        self.blockchain = Blockchain()
        self.setup_data_directory()

    def setup_data_directory(self):
        """
        Sets up the data directory for storing blockchain information.
        """
        node_path = os.path.join(self.data_dir, self.node_id)
        if not os.path.exists(node_path):
            os.makedirs(node_path)
            print(f"Data directory created for node {self.node_id} at {node_path}")
        else:
            print(f"Data directory already exists for node {self.node_id} at {node_path}")

    def save_blockchain_state(self):
        """
        Saves the current blockchain state to a file.
        """
        node_path = os.path.join(self.data_dir, self.node_id)
        blockchain_file = os.path.join(node_path, "blockchain.json")
        blockchain_data = [{
            "index": block.index,
            "previous_hash": block.previous_hash,
            "timestamp": block.timestamp,
            "data": block.data,
            "nonce": block.nonce,
        } for block in self.blockchain.chain]
        
        with open(blockchain_file, 'w') as file:
            json.dump(blockchain_data, file, indent=4)
        print(f"Blockchain state saved for node {self.node_id}.")

    def load_blockchain_state(self):
        """
        Loads the blockchain state from a file if it exists.
        """
        node_path = os.path.join(self.data_dir, self.node_id)
        blockchain_file = os.path.join(node_path, "blockchain.json")
        
        if os.path.exists(blockchain_file):
            with open(blockchain_file, 'r') as file:
                blockchain_data = json.load(file)
                
                # Recreate blocks without providing the hash, let the block class handle it
                self.blockchain.chain = [
                    Block(
                        index=block["index"],
                        previous_hash=block["previous_hash"],
                        timestamp=block["timestamp"],
                        data=block["data"],
                        nonce=block["nonce"]
                    ) for block in blockchain_data
                ]
            print(f"Blockchain state loaded for node {self.node_id}.")
        else:
            print(f"No blockchain state found for node {self.node_id}. Starting with genesis block.")

    def initiate_consensus(self, peer_blockchains: List[Blockchain]):
        """
        Initiates the consensus mechanism for the node to determine the correct chain.
        :param peer_blockchains: List of blockchains from peer nodes.
        """
        # Pass Blockchain objects, not just the chains
        all_blockchains = peer_blockchains + [self.blockchain]
        consensus_mechanism = ConsensusMechanism(nodes=all_blockchains)
        self.blockchain.chain = consensus_mechanism.longest_chain_rule().chain  # Set the longest chain
        print(f"Consensus applied for node {self.node_id}, updated chain length: {len(self.blockchain.chain)}")

# Example usage
if __name__ == "__main__":
    # Initialize node1 with some peers
    node1 = NodeInitializer(node_id="node1", peers=["node2", "node3"])
    node1.save_blockchain_state()
    node1.load_blockchain_state()

    # Simulate peers
    peer1 = Blockchain()
    peer1.add_block("Peer1 - Block 1")
    peer1.add_block("Peer1 - Block 2")

    peer2 = Blockchain()
    peer2.add_block("Peer2 - Block 1")

    # Apply consensus
    node1.initiate_consensus([peer1, peer2])
    node1.save_blockchain_state()
