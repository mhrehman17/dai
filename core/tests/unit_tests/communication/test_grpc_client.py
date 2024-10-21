import unittest
from unittest.mock import patch, MagicMock
import grpc
import core.communication.grpc_server_pb2 as pb2
import core.communication.grpc_server_pb2_grpc as pb2_grpc
from core.communication.grpc_client import BlockchainClient


class BlockchainClientTest(unittest.TestCase):

    @patch('core.communication.grpc_server_pb2_grpc.BlockchainStub')
    def setUp(self, MockBlockchainStub):
        # Set up a mock gRPC channel and stub
        self.mock_stub = MockBlockchainStub.return_value
        self.client = BlockchainClient(server_address="localhost:50051")

    def test_get_blockchain_state_empty(self):
        # Mocking an empty blockchain response
        empty_response = pb2.BlockchainState(blocks=[])
        self.mock_stub.GetBlockchainState.return_value = empty_response

        # Call the method
        blockchain_state = self.client.get_blockchain_state()

        # Assertions
        self.mock_stub.GetBlockchainState.assert_called_once_with(pb2.Empty())
        self.assertEqual(len(blockchain_state), 0)
        print("test_get_blockchain_state_empty passed")

    def test_get_blockchain_state_with_blocks(self):
        # Mocking a response with multiple blocks
        mock_blocks = [
            pb2.Block(index=0, previous_hash="0", timestamp="1234567890", data="Genesis Block", nonce=0,
                      hash="genesis_hash"),
            pb2.Block(index=1, previous_hash="genesis_hash", timestamp="1234567891", data="Block 1", nonce=1234,
                      hash="hash_1")
        ]
        response = pb2.BlockchainState(blocks=mock_blocks)
        self.mock_stub.GetBlockchainState.return_value = response

        # Call the method
        blockchain_state = self.client.get_blockchain_state()

        # Assertions
        self.mock_stub.GetBlockchainState.assert_called_once_with(pb2.Empty())
        self.assertEqual(len(blockchain_state), 2)
        self.assertEqual(blockchain_state[0].data, "Genesis Block")
        self.assertEqual(blockchain_state[1].data, "Block 1")
        print("test_get_blockchain_state_with_blocks passed")

    def test_add_block_success(self):
        # Mocking a successful response to add a block
        add_block_response = pb2.BlockResponse(success=True)
        self.mock_stub.AddBlock.return_value = add_block_response

        # Call the method to add a block
        self.client.add_block(data="New Block Data")

        # Assertions
        self.mock_stub.AddBlock.assert_called_once()
        request = self.mock_stub.AddBlock.call_args[0][0]
        self.assertEqual(request.data, "New Block Data")
        print("test_add_block_success passed")

    def test_add_block_failure(self):
        # Mocking a failed response to add a block
        add_block_response = pb2.BlockResponse(success=False)
        self.mock_stub.AddBlock.return_value = add_block_response

        # Call the method to add a block
        self.client.add_block(data="Failed Block Data")

        # Assertions
        self.mock_stub.AddBlock.assert_called_once()
        request = self.mock_stub.AddBlock.call_args[0][0]
        self.assertEqual(request.data, "Failed Block Data")
        print("test_add_block_failure passed")

    def test_rpc_error_handling(self):
        # Simulate an RPC error
        rpc_error = grpc.RpcError()
        rpc_error.code = MagicMock(return_value=grpc.StatusCode.UNAVAILABLE)
        rpc_error.details = MagicMock(return_value="Service unavailable")
        
        self.mock_stub.GetBlockchainState.side_effect = rpc_error

        # Call the method to test RPC error handling
        blockchain_state = self.client.get_blockchain_state()

        # Assertions
        self.mock_stub.GetBlockchainState.assert_called_once()
        self.assertIsNone(blockchain_state)
        print("test_rpc_error_handling passed")


if __name__ == '__main__':
    unittest.main()
