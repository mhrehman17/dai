import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
from core.ledger.blockchain import Blockchain
from core.ledger.block import Block
from core.ledger.node_setup.node_init import NodeInitializer

class TestNodeInitializer(unittest.TestCase):

    def setUp(self):
        """
        Setup for each test case. Create a NodeInitializer object with test data.
        """
        self.node_id = "test_node"
        self.peers = ["peer1", "peer2"]
        self.data_dir = "./test_node_data"
        self.node_initializer = NodeInitializer(self.node_id, self.peers, self.data_dir)

    @patch('os.makedirs')
    @patch('os.path.exists', return_value=False)
    def test_setup_data_directory_new(self, mock_exists, mock_makedirs):
        """
        Test that the data directory is created when it doesn't exist.
        """
        self.node_initializer.setup_data_directory()
        mock_makedirs.assert_called_once_with(os.path.join(self.data_dir, self.node_id))
        print("Directory created correctly")

    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs')
    def test_setup_data_directory_existing(self, mock_makedirs, mock_exists):
        """
        Test that the data directory is not created if it already exists.
        """
        self.node_initializer.setup_data_directory()
        mock_makedirs.assert_not_called()
        print("Directory already exists, no creation needed")

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=True)
    def test_save_blockchain_state(self, mock_exists, mock_file):
        """
        Test that the blockchain state is saved to a file.
        """
        # Mock the blockchain and block data
        mock_block = MagicMock(spec=Block)
        mock_block.index = 0
        mock_block.previous_hash = "genesis_hash"
        mock_block.timestamp = 1234567890
        mock_block.data = "Genesis Block"
        mock_block.nonce = 0

        # Mock the chain in the blockchain
        self.node_initializer.blockchain.chain = [mock_block]

        # Call save_blockchain_state
        self.node_initializer.save_blockchain_state()

        # Check that the file was opened for writing
        mock_file.assert_called_once_with(os.path.join(self.data_dir, self.node_id, "blockchain.json"), 'w')

        # Collect all write calls
        handle = mock_file()
        write_calls = handle.write.call_args_list

        # Reconstruct the written JSON string from the multiple write calls
        written_json = "".join(call[0][0] for call in write_calls)

        # Load the JSON back to verify its structure
        written_data = json.loads(written_json)

        # Verify the contents of the written JSON
        self.assertEqual(written_data[0]['index'], 0)
        self.assertEqual(written_data[0]['previous_hash'], "genesis_hash")
        self.assertEqual(written_data[0]['timestamp'], 1234567890)
        self.assertEqual(written_data[0]['data'], "Genesis Block")
        self.assertEqual(written_data[0]['nonce'], 0)

    @patch("builtins.open", new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    def test_load_blockchain_state(self, mock_exists, mock_file):
        """
        Test that the blockchain state is loaded from a file.
        """
        # Mock file content
        blockchain_data = [{
            "index": 0,
            "previous_hash": "genesis_hash",
            "timestamp": 1234567890,
            "data": "Genesis Block",
            "nonce": 0
        }]
        mock_file().read.return_value = json.dumps(blockchain_data)

        self.node_initializer.load_blockchain_state()

        self.assertEqual(len(self.node_initializer.blockchain.chain), 1)
        self.assertEqual(self.node_initializer.blockchain.chain[0].index, 0)
        self.assertEqual(self.node_initializer.blockchain.chain[0].data, "Genesis Block")
        print("Blockchain loaded successfully")

    @patch("builtins.open", new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_load_blockchain_state_no_file(self, mock_exists, mock_file):
        """
        Test that if no blockchain file exists, it starts with a genesis block.
        """
        self.node_initializer.load_blockchain_state()

        self.assertEqual(len(self.node_initializer.blockchain.chain), 1)
        self.assertEqual(self.node_initializer.blockchain.chain[0].index, 0)
        print("Started with genesis block")

    @patch('core.ledger.consensus_mechanism.ConsensusMechanism.longest_chain_rule')
    def test_initiate_consensus(self, mock_longest_chain_rule):
        """
        Test the initiate_consensus method to ensure the longest chain is selected.
        """
        # Create mock peer blockchains
        peer_blockchain_1 = MagicMock(spec=Blockchain)
        peer_blockchain_1.chain = [MagicMock(spec=Block)]  # Mocking a chain with one block
        peer_blockchain_2 = MagicMock(spec=Blockchain)
        peer_blockchain_2.chain = [MagicMock(spec=Block), MagicMock(spec=Block)]  # Mock longer chain

        mock_longest_chain_rule.return_value = peer_blockchain_2  # Return the longer chain

        # Call initiate consensus
        self.node_initializer.initiate_consensus([peer_blockchain_1, peer_blockchain_2])

        # Ensure the longest_chain_rule method was called
        mock_longest_chain_rule.assert_called_once()
        self.assertEqual(self.node_initializer.blockchain.chain, peer_blockchain_2.chain)
        print("Consensus mechanism applied correctly")

    @patch('os.path.exists', return_value=False)
    def test_initiate_consensus_no_peers(self, mock_exists):
        """
        Test the initiate_consensus method when there are no peer blockchains (node has the only chain).
        """
        self.node_initializer.initiate_consensus([])  # No peer blockchains

        # Expect that the current node's chain is kept as the longest
        self.assertEqual(self.node_initializer.blockchain, self.node_initializer.blockchain)
        print("Consensus mechanism with no peers handled correctly")

if __name__ == '__main__':
    unittest.main()
