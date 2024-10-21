import unittest
from unittest.mock import patch, MagicMock
from core.ledger.blockchain_ledger import Blockchain, Block
from core.ledger.consensus_mechanism import ConsensusMechanism


class TestConsensusMechanism(unittest.TestCase):
    
    def setUp(self):
        """
        Set up blockchains for the nodes before each test.
        """
        self.node1 = Blockchain()
        self.node2 = Blockchain()
        self.node3 = Blockchain()

        # Add some blocks to simulate different chain lengths
        self.node1.add_block("Node 1 - Block 1")
        self.node1.add_block("Node 1 - Block 2")

        self.node2.add_block("Node 2 - Block 1")

        self.node3.add_block("Node 3 - Block 1")
        self.node3.add_block("Node 3 - Block 2")
        self.node3.add_block("Node 3 - Block 3")

        # Initialize consensus mechanism with nodes
        self.consensus = ConsensusMechanism([self.node1, self.node2, self.node3])

    def test_longest_chain_rule(self):
        """
        Test the longest_chain_rule to ensure it selects the longest chain and updates other nodes.
        """
        longest_chain_node = self.consensus.longest_chain_rule()

        # The longest chain should be from node3
        self.assertEqual(longest_chain_node, self.node3)
        self.assertEqual(len(longest_chain_node.chain), 4)  # Genesis block + 3 blocks

        # Ensure other nodes' chains are updated to the longest chain
        for node in [self.node1, self.node2]:
            self.assertEqual(len(node.chain), 4)
            self.assertEqual(node.chain, self.node3.chain)

    @patch('core.ledger.blockchain_ledger.Blockchain.is_chain_valid', return_value=False)
    def test_longest_chain_rule_invalid_chain(self, mock_is_chain_valid):
        """
        Test that an invalid chain is not selected as the longest chain.
        """
        longest_chain_node = self.consensus.longest_chain_rule()

        # The longest valid chain should be from node1 since others are invalid
        self.assertEqual(longest_chain_node, self.node1)
        self.assertEqual(len(longest_chain_node.chain), 3)  # Genesis block + 2 blocks

        # Ensure other nodes' chains are updated to node1's chain
        for node in [self.node2, self.node3]:
            self.assertEqual(node.chain, self.node1.chain)

    def test_proof_of_stake(self):
        """
        Test the proof_of_stake method to ensure the node with the highest stake is selected.
        """
        stake_distribution = {
            id(self.node1): 50,
            id(self.node2): 30,
            id(self.node3): 20
        }

        selected_node = self.consensus.proof_of_stake(stake_distribution)

        # The node with the highest stake (node1) should be selected
        self.assertEqual(selected_node, self.node1)

    def test_proof_of_stake_equal_stakes(self):
        """
        Test the proof_of_stake method when nodes have equal stakes.
        """
        stake_distribution = {
            id(self.node1): 50,
            id(self.node2): 50,
            id(self.node3): 50
        }

        selected_node = self.consensus.proof_of_stake(stake_distribution)

        # In case of equal stakes, the first node should be selected
        self.assertEqual(selected_node, self.node1)

    def test_proof_of_authority(self):
        """
        Test the proof_of_authority method to ensure the correct authority node is selected.
        """
        authorities = [id(self.node1), id(self.node2)]

        selected_node = self.consensus.proof_of_authority(authorities)

        # The first authority node (node1) should be selected
        self.assertEqual(selected_node, self.node1)

    def test_proof_of_authority_invalid_authority(self):
        """
        Test the proof_of_authority method with an invalid authority node.
        """
        authorities = [id(self.node1), 999999]  # Second authority does not exist

        selected_node = self.consensus.proof_of_authority(authorities)

        # Only the valid authority node (node1) should be selected
        self.assertEqual(selected_node, self.node1)

    def test_chain_update_after_longest_chain(self):
        """
        Test that chains are correctly updated after the longest_chain_rule is applied.
        """
        # Apply the longest chain rule
        self.consensus.longest_chain_rule()

        # Ensure that node1 and node2 have the same chain as node3 (the longest chain)
        for node in [self.node1, self.node2]:
            self.assertEqual(node.chain, self.node3.chain)
            self.assertEqual(len(node.chain), len(self.node3.chain))

    def test_no_chain_update_if_all_chains_equal(self):
        """
        Test that no update happens if all chains are of equal length and valid.
        """
        # Make all chains the same length
        self.node1.add_block("Node 1 - Block 3")
        self.node2.add_block("Node 2 - Block 3")

        # Apply consensus (should not replace the chain since they are all equal length)
        selected_node = self.consensus.longest_chain_rule()

        # Ensure no chains are replaced
        self.assertEqual(selected_node.chain, self.node1.chain)

    @patch('core.ledger.blockchain_ledger.Blockchain.is_chain_valid', return_value=True)
    def test_longest_chain_with_invalid_nodes(self, mock_is_chain_valid):
        """
        Test longest_chain_rule when there are nodes with invalid chains.
        """
        # Simulate that node2 has an invalid chain
        mock_is_chain_valid.side_effect = [True, False, True]

        selected_node = self.consensus.longest_chain_rule()

        # The longest valid chain should be selected (node3's chain)
        self.assertEqual(selected_node, self.node3)
        self.assertEqual(len(selected_node.chain), 4)

if __name__ == "__main__":
    unittest.main()
