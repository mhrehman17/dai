import hashlib
import time
from typing import List
from core.ledger.block import Block

class Blockchain:
    def __init__(self):
        """
        Initializes the blockchain.
        """
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Creates the genesis block and adds it to the chain.
        """
        genesis_block = Block(index=0, previous_hash="0", timestamp=time.time(), data="Genesis Block")
        self.chain.append(genesis_block)
        print(f"Genesis block created: {genesis_block.hash}")

    def get_last_block(self) -> Block:
        """
        Retrieves the last block in the chain.
        :return: The last block in the blockchain.
        """
        return self.chain[-1]

    def add_block(self, data: str):
        """
        Adds a new block to the blockchain after performing proof of work.
        :param data: The data to be stored in the block.
        """
        last_block = self.get_last_block()
        new_block = Block(index=last_block.index + 1, previous_hash=last_block.hash, timestamp=time.time(), data=data)
        new_block = self.proof_of_work(new_block)
        self.chain.append(new_block)
        print(f"Block {new_block.index} added with hash: {new_block.hash}")

    def proof_of_work(self, block: Block, difficulty: int = 4) -> Block:
        """
        Performs the proof of work algorithm to find a valid nonce for the block.
        :param block: The block that needs proof of work.
        :param difficulty: The difficulty level for mining the block.
        :return: The block with a valid nonce that meets the difficulty criteria.
        """
        prefix = "0" * difficulty
        while not block.hash.startswith(prefix):
            block.nonce += 1
            block.hash = block.compute_hash()
        return block

    def is_chain_valid(self) -> bool:
        """
        Validates the blockchain to ensure integrity.
        :return: True if the blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is correct
            if current_block.hash != current_block.compute_hash():
                print(f"Invalid block hash at index {i}")
                return False

            # Check if the previous hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid chain link between block {i-1} and block {i}")
                return False
        return True

    def consensus(self, chains: List[List[Block]]) -> List[Block]:
        """
        Implements a consensus mechanism to replace the current chain with the longest valid chain.
        :param chains: A list of chains from other nodes in the network.
        :return: The longest valid chain that replaces the current chain if applicable.
        """
        longest_chain = self.chain
        max_length = len(self.chain)

        for chain in chains:
            if len(chain) > max_length and self.is_chain_valid_external(chain):
                longest_chain = chain
                max_length = len(chain)

        # Replace the current chain only if we find a strictly longer valid chain
        if longest_chain != self.chain:
            self.chain = longest_chain
            print("Chain replaced with the longest valid chain from the network.")
        else:
            print("Current chain is already the longest valid chain, or chains are of equal length.")
        return self.chain

    def is_chain_valid_external(self, chain: List[Block]) -> bool:
        """
        Validates an external chain to ensure integrity.
        :param chain: The chain to validate.
        :return: True if the chain is valid, False otherwise.
        """
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            # Check if the current block's hash is correct
            if current_block.hash != current_block.compute_hash():
                print(f"Invalid block hash at index {i} in the external chain")
                return False

            # Check if the previous hash matches the hash of the previous block
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid chain link between block {i-1} and block {i} in the external chain")
                return False
        return True

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add blocks to the blockchain
    blockchain.add_block(data="Block 1 Data")
    blockchain.add_block(data="Block 2 Data")

    # Validate the blockchain
    is_valid = blockchain.is_chain_valid()
    print(f"Blockchain valid: {is_valid}")

    # Create another chain to simulate a network of blockchains
    another_blockchain = Blockchain()
    another_blockchain.add_block(data="Block 1 Data from another chain")
    another_blockchain.add_block(data="Block 2 Data from another chain")

    # Apply consensus
    blockchain.consensus([another_blockchain.chain])

    # Print the blockchain
    for block in blockchain.chain:
        print(f"Index: {block.index}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Data: {block.data}")
