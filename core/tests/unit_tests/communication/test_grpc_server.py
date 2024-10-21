import unittest
from unittest.mock import MagicMock
import grpc
from concurrent import futures
import core.communication.grpc_server_pb2 as pb2
import core.communication.grpc_server_pb2_grpc as pb2_grpc
from core.ledger.blockchain_ledger import Blockchain
from core.communication.grpc_server import BlockchainService


class BlockchainServiceTest(unittest.TestCase):

    def setUp(self):
        # Set up a new blockchain instance and gRPC server before each test
        self.blockchain = Blockchain()  # A new instance for each test to avoid shared state
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_BlockchainServicer_to_server(BlockchainService(self.blockchain), self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()

        # Set up the gRPC channel and stub for client-side interaction with the server
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = pb2_grpc.BlockchainStub(self.channel)

    def tearDown(self):
        # Stop the gRPC server after each test
        self.server.stop(0)
        self.channel.close()

    def test_get_blockchain_state_empty(self):
        # Test retrieving the blockchain state when no blocks have been added (only genesis block)
        request = pb2.Empty()
        response = self.stub.GetBlockchainState(request)
        # Since the blockchain always starts with a genesis block, assert that it has 1 block
        self.assertEqual(len(response.blocks), 1)

    def test_add_block_and_get_blockchain_state(self):
        # Test adding a block and then retrieving the blockchain state
        data = "Test data for block 1"
        add_request = pb2.BlockRequest(data=data)
        add_response = self.stub.AddBlock(add_request)
        self.assertTrue(add_response.success)

        # Now retrieve the blockchain state
        get_request = pb2.Empty()
        get_response = self.stub.GetBlockchainState(get_request)
        # Since the genesis block is always present, we should have 2 blocks in total
        self.assertEqual(len(get_response.blocks), 2)

    def test_multiple_blocks(self):
        # Test adding multiple blocks and verifying the blockchain state
        block_data_list = ["Block data 1", "Block data 2", "Block data 3"]
        for data in block_data_list:
            add_request = pb2.BlockRequest(data=data)
            add_response = self.stub.AddBlock(add_request)
            self.assertTrue(add_response.success)

        # Now retrieve the blockchain state
        get_request = pb2.Empty()
        get_response = self.stub.GetBlockchainState(get_request)
        # Since the genesis block is always present, we should have len(block_data_list) + 1 blocks in total
        self.assertEqual(len(get_response.blocks), len(block_data_list) + 1)


if __name__ == "__main__":
    unittest.main()
