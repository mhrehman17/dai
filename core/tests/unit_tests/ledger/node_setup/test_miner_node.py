import unittest
from unittest.mock import patch, MagicMock
import time
from core.ledger.node_setup.node_init import NodeInitializer
from core.ledger.blockchain import Blockchain
from core.ledger.block import Block
from core.ledger.node_setup.miner_node import MinerNode

class TestMinerNode(unittest.TestCase):
    def setUp(self):
        """
        Set up the test by initializing a MinerNode with mock peers and blockchain.
        """
        self.miner_node = MinerNode(node_id="test_miner", peers=["node2", "node3"], mining_interval=1)
        self.miner_node.blockchain = MagicMock(Blockchain())  # Mock the blockchain

    @patch('time.sleep', side_effect=lambda _: None)  # Mock sleep to avoid delay
    @patch('core.ledger.node_setup.node_init.Blockchain.add_block')
    @patch('core.ledger.node_setup.node_init.NodeInitializer.save_blockchain_state')
    def test_mine_new_block(self, mock_save_blockchain_state, mock_add_block, mock_sleep):
        """
        Test the mine_new_block method to ensure a new block is mined and added.
        """
        mock_last_block = MagicMock(Block)
        mock_last_block.hash = "dummyhash"
        self.miner_node.blockchain.get_last_block.return_value = mock_last_block

        # Call mine_new_block and check the behavior
        self.miner_node.mine_new_block()

        # Check that add_block and save_blockchain_state were called
        mock_add_block.assert_called_once_with(f"Mined by test_miner at {time.time()}")
        mock_save_blockchain_state.assert_called_once()

    @patch('time.sleep', side_effect=lambda _: None)  # Mock sleep to simulate time passage
    @patch('core.ledger.node_setup.node_init.Blockchain.add_block')
    @patch('core.ledger.node_setup.node_init.NodeInitializer.save_blockchain_state')
    def test_start_mining(self, mock_save_blockchain_state, mock_add_block, mock_sleep):
        """
        Test that mining starts and blocks are mined.
        """
        # Start mining
        self.miner_node.start_mining()

        # Simulate some mining time
        time.sleep(3 * self.miner_node.mining_interval)

        # Stop mining
        self.miner_node.stop_mining()

        # Check that add_block was called at least 3 times
        self.assertGreaterEqual(mock_add_block.call_count, 3)

        # Ensure save_blockchain_state was called
        self.assertGreaterEqual(mock_save_blockchain_state.call_count, 3)

    @patch('time.sleep', side_effect=lambda _: None)  # Mock sleep to simulate time passage
    @patch('core.ledger.node_setup.node_init.Blockchain.add_block')
    @patch('core.ledger.node_setup.node_init.NodeInitializer.save_blockchain_state')
    def test_mining_interval(self, mock_save_blockchain_state, mock_add_block, mock_sleep):
        """
        Test that blocks are mined at the correct interval.
        """
        # Start mining
        self.miner_node.start_mining()

        # Simulate sleep to let mining run for a while (e.g., 5 intervals)
        expected_blocks = 5
        for _ in range(expected_blocks):
            time.sleep(self.miner_node.mining_interval)

        # Stop mining
        self.miner_node.stop_mining()

        # Check that add_block was called 5 times
        self.assertEqual(mock_add_block.call_count, expected_blocks)

        # Ensure save_blockchain_state was called after each block addition
        self.assertEqual(mock_save_blockchain_state.call_count, expected_blocks)

    @patch('time.sleep', side_effect=lambda _: None)  # Mock sleep to avoid delay
    def test_stop_mining(self, mock_sleep):
        """
        Test stopping the mining process.
        """
        # Start mining
        self.miner_node.start_mining()

        # Simulate some mining time
        time.sleep(self.miner_node.mining_interval)

        # Stop mining
        self.miner_node.stop_mining()

        # Check that mining is stopped
        self.assertFalse(self.miner_node.is_mining)

    @patch('time.sleep', side_effect=lambda _: None)  # Mock sleep to avoid delay
    @patch('core.ledger.node_setup.node_init.Blockchain.add_block')
    def test_mine_new_block_called_in_thread(self, mock_add_block, mock_sleep):
        """
        Test that mining happens in a separate thread and add_block is called.
        """
        # Start mining
        self.miner_node.start_mining()

        # Simulate some mining time
        time.sleep(2 * self.miner_node.mining_interval)

        # Stop mining
        self.miner_node.stop_mining()

        # Check that add_block was called at least once in the mining thread
        self.assertGreaterEqual(mock_add_block.call_count, 2)

if __name__ == '__main__':
    unittest.main()
