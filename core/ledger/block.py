import hashlib
import time
from typing import List

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: str, nonce: int = 0):
        """
        Initializes a blockchain block.
        :param index: Index of the block in the blockchain.
        :param previous_hash: Hash of the previous block in the chain.
        :param timestamp: Time when the block was created.
        :param data: Data to be stored in the block.
        :param nonce: The nonce value used for proof of work.
        """
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Computes the hash of the block using SHA-256.
        :return: A SHA-256 hash of the block.
        """
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

