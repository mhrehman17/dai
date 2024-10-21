import hashlib
import time
from typing import List
from core.ledger.blockchain import Blockchain
from core.ledger.block import Block

class ConsensusMechanism:
    def __init__(self, nodes: List[Blockchain]):
        """
        Initializes the consensus mechanism for blockchain nodes in a network.
        :param nodes: A list of Blockchain instances representing nodes in the network.
        """
        self.nodes = nodes

    def longest_chain_rule(self) -> Blockchain:
        """
        Applies the longest chain rule to achieve consensus among nodes.
        :return: The Blockchain instance with the longest valid chain.
        """
        # Start by assuming the first node has the longest chain
        longest_chain_node = self.nodes[0]
        
        for node in self.nodes:
            # Find the node with the longest valid chain
            if len(node.chain) > len(longest_chain_node.chain) and node.is_chain_valid():
                longest_chain_node = node

        # Set the consensus chain as the longest chain for all nodes
        for node in self.nodes:
            if node.chain != longest_chain_node.chain:
                node.chain = longest_chain_node.chain  # Update chain for the node
                print(f"Node {id(node)} updated its chain to the longest chain.")

        # Return the node with the longest chain (not just the chain itself)
        return longest_chain_node

    def proof_of_stake(self, stake_distribution: dict) -> Blockchain:
        """
        Applies a simple Proof of Stake mechanism for consensus.
        The node with the highest stake is selected to add the next block.
        :param stake_distribution: A dictionary mapping node ids to their respective stakes.
        :return: The blockchain representing the selected node.
        """
        # Select the node with the maximum stake
        highest_stake_node = max(stake_distribution, key=stake_distribution.get)
        print(f"Node {highest_stake_node} selected to add the next block based on Proof of Stake.")

        selected_node = next(node for node in self.nodes if id(node) == highest_stake_node)
        return selected_node

    def proof_of_authority(self, authorities: List[int]) -> Blockchain:
        """
        Implements Proof of Authority to select a trusted authority node to validate the chain.
        :param authorities: A list of node ids representing authority nodes.
        :return: The blockchain representing the selected authority node.
        """
        # Select the first authority node from the list for simplicity
        selected_authority = authorities[0]
        print(f"Node {selected_authority} selected to validate and add new blocks as authority.")

        selected_node = next(node for node in self.nodes if id(node) == selected_authority)
        return selected_node

# Example usage
if __name__ == "__main__":
    # Create blockchains for multiple nodes
    node1 = Blockchain()
    node2 = Blockchain()
    node3 = Blockchain()

    # Add some blocks to the nodes to simulate independent blockchains
    node1.add_block(data="Node 1 - Block 1")
    node1.add_block(data="Node 1 - Block 2")

    node2.add_block(data="Node 2 - Block 1")

    node3.add_block(data="Node 3 - Block 1")
    node3.add_block(data="Node 3 - Block 2")
    node3.add_block(data="Node 3 - Block 3")

    # Initialize the consensus mechanism
    nodes = [node1, node2, node3]
    consensus = ConsensusMechanism(nodes=nodes)

    # Apply the longest chain rule
    longest_chain_node = consensus.longest_chain_rule()
    print(f"Longest chain selected from Node {id(longest_chain_node)} with length: {len(longest_chain_node.chain)}")

    # Example of Proof of Stake consensus
    stake_distribution = {
        id(node1): 50,
        id(node2): 30,
        id(node3): 20
    }
    selected_node_pos = consensus.proof_of_stake(stake_distribution)
    print(f"Node {id(selected_node_pos)} selected for the next block based on stake.")

    # Example of Proof of Authority consensus
    authorities = [id(node1), id(node2)]
    selected_node_poa = consensus.proof_of_authority(authorities)
    print(f"Node {id(selected_node_poa)} selected as authority for adding blocks.")
