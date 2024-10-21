import unittest
from unittest.mock import patch, MagicMock
import time
from core.ledger.blockchain import Blockchain
from core.ledger.node_setup.node_init import NodeInitializer
from core.ledger.consensus_mechanism import ConsensusMechanism
from core.ledger.node_setup.validator_node import ValidatorNode

class TestValidatorNode(unittest.TestCase):

    def setUp(self):
        """
        Set up a ValidatorNode instance for each test.
        """
        self.node_id = "validator1"
        self.peers = ["peer1", "peer2"]
        self.data_dir = "./test_node_data"
        self.validation_interval = 1  # Use a short interval for testing
        self.validator_node = ValidatorNode(self.node_id, self.peers, self.data_dir, self.validation_interval)

    @patch('core.ledger.blockchain.Blockchain.is_chain_valid', return_value=True)
    def test_start_validation(self, mock_is_chain_valid):
        """
        Test that validation starts correctly and runs validation checks.
        """
        self.validator_node.start_validation()
        time.sleep(2)  # Allow validation to run
        self.validator_node.stop_validation()

        self.assertTrue(self.validator_node.is_validating, "Validation did not start correctly.")
        mock_is_chain_valid.assert_called()

    def test_stop_validation(self):
        """
        Test that validation stops correctly.
        """
        self.validator_node.start_validation()
        time.sleep(1)
        self.validator_node.stop_validation()

        self.assertFalse(self.validator_node.is_validating, "Validation did not stop correctly.")

    @patch('core.ledger.blockchain.Blockchain.is_chain_valid', return_value=False)
    @patch('core.ledger.validator_node.ValidatorNode.initiate_consensus_with_peers')
    def test_initiate_consensus_on_invalid_chain(self, mock_initiate_consensus, mock_is_chain_valid):
        """
        Test that consensus is initiated when the chain is found to be invalid.
        """
        self.validator_node.start_validation()
        time.sleep(2)  # Let the validation run once
        self.validator_node.stop_validation()

        mock_initiate_consensus.assert_called_once()
        mock_is_chain_valid.assert_called()

    @patch('core.ledger.validator_node.ValidatorNode.get_peer_blockchains')
    @patch('core.ledger.consensus_mechanism.ConsensusMechanism.longest_chain_rule')
    def test_initiate_consensus_with_peers(self, mock_longest_chain_rule, mock_get_peer_blockchains):
        """
        Test that the consensus mechanism is initiated with peer blockchains.
        """
        # Create mock peer blockchains
        peer_blockchain_1 = MagicMock(spec=Blockchain)
        peer_blockchain_2 = MagicMock(spec=Blockchain)
        mock_get_peer_blockchains.return_value = [peer_blockchain_1, peer_blockchain_2]

        # Call initiate consensus with peers
        self.validator_node.initiate_consensus_with_peers()

        # Verify consensus was initiated with the correct blockchains
        mock_get_peer_blockchains.assert_called_once()
        mock_longest_chain_rule.assert_called_once()

    def test_get_peer_blockchains(self):
        """
        Test that the simulated fetching of peer blockchains works as expected.
        """
        peer_blockchains = self.validator_node.get_peer_blockchains()

        # Check that the correct number of peer blockchains is returned
        self.assertEqual(len(peer_blockchains), len(self.peers))

        # Check that each blockchain has the expected data
        for i, peer_blockchain in enumerate(peer_blockchains):
            self.assertEqual(peer_blockchain.get_last_block().data, f"Block from {self.peers[i]} - Simulated for consensus")

    @patch('core.ledger.blockchain.Blockchain.add_block')
    def test_blockchain_add_block(self, mock_add_block):
        """
        Test that new blocks are added to the blockchain correctly during consensus.
        """
        # Call method to fetch peer blockchains and check if blocks are added
        self.validator_node.get_peer_blockchains()

        # Ensure blocks are added to peer blockchains
        mock_add_block.assert_called()

if __name__ == '__main__':
    unittest.main()
