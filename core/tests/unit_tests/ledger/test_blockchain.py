import unittest
from unittest.mock import MagicMock
import time
from core.ledger.block import Block
from core.ledger.blockchain import Blockchain

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """
        Setup a new Blockchain instance before each test.
        """
        self.blockchain = Blockchain()

    def test_genesis_block_creation(self):
        """
        Test if the genesis block is created correctly when the blockchain is initialized.
        """
        genesis_block = self.blockchain.chain[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, "0")
        self.assertEqual(genesis_block.data, "Genesis Block")
        # Removing the proof of work requirement for genesis block
        # as genesis blocks are typically predefined and not mined.
        self.assertTrue(genesis_block.hash)  # Ensure the genesis block has a hash

    def test_add_block(self):
        """
        Test adding a new block to the blockchain.
        """
        initial_length = len(self.blockchain.chain)
        self.blockchain.add_block("Test Block")
        self.assertEqual(len(self.blockchain.chain), initial_length + 1)

        # Check block data and ensure it's valid
        last_block = self.blockchain.get_last_block()
        self.assertEqual(last_block.data, "Test Block")
        self.assertTrue(last_block.hash.startswith("0" * 4))  # Proof of work

    def test_proof_of_work(self):
        """
        Test the proof of work algorithm.
        """
        new_block = Block(index=1, previous_hash="0", timestamp=time.time(), data="Test Block")
        new_block = self.blockchain.proof_of_work(new_block)

        # Ensure that the block has a valid proof of work
        self.assertTrue(new_block.hash.startswith("0" * 4))

    def test_is_chain_valid(self):
        """
        Test the validity of the blockchain.
        """
        # Add valid blocks to the blockchain
        self.blockchain.add_block("Block 1 Data")
        self.blockchain.add_block("Block 2 Data")

        # Ensure the blockchain is valid
        self.assertTrue(self.blockchain.is_chain_valid())

        # Tamper with the blockchain and check invalidity
        self.blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.is_chain_valid())

    def test_consensus_with_longer_chain(self):
        """
        Test that the consensus mechanism correctly selects the longest valid chain.
        """
        another_blockchain = Blockchain()
        another_blockchain.add_block("Block 1 Data from another chain")
        another_blockchain.add_block("Block 2 Data from another chain")
        another_blockchain.add_block("Block 3 Data from another chain")  # Longer chain

        self.blockchain.consensus([another_blockchain.chain])

        # Ensure the chain has been replaced by the longer one
        self.assertEqual(len(self.blockchain.chain), len(another_blockchain.chain))

    def test_consensus_with_same_length_chain(self):
        """
        Test the consensus mechanism with a chain of the same length.
        """
        # Add one block to the current chain
        self.blockchain.add_block("Block 1 Data")

        # Create another blockchain with the same length (one additional block)
        another_blockchain = Blockchain()
        another_blockchain.add_block("Block 1 Data from another chain")

        # Test with the same length chain, expect the chain not to be replaced
        original_last_block = self.blockchain.get_last_block().data
        self.blockchain.consensus([another_blockchain.chain])

        # Since the chains are of equal length, the original chain should be retained
        self.assertEqual(self.blockchain.get_last_block().data, original_last_block)


    def test_is_chain_valid_external(self):
        """
        Test the validation of an external chain.
        """
        another_blockchain = Blockchain()
        another_blockchain.add_block("Block 1 Data from another chain")

        # Test valid external chain
        self.assertTrue(self.blockchain.is_chain_valid_external(another_blockchain.chain))

        # Tamper with the external chain and check invalidity
        another_blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.is_chain_valid_external(another_blockchain.chain))

    def test_blockchain_invalid_block(self):
        """
        Test if the blockchain detects an invalid block.
        """
        # Add a valid block
        self.blockchain.add_block("Valid Block Data")

        # Manually tamper with the block's hash
        self.blockchain.chain[1].hash = "0000000000000000"

        # The chain should now be invalid
        self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
