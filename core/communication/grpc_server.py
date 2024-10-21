import grpc
from concurrent import futures
import time
import core.communication.grpc_server_pb2 as pb2
import core.communication.grpc_server_pb2_grpc as pb2_grpc
from core.ledger.blockchain_ledger import Blockchain

class BlockchainService(pb2_grpc.BlockchainServicer):
    def __init__(self, blockchain: Blockchain):
        """
        Initializes the BlockchainService with an instance of Blockchain.
        :param blockchain: The blockchain instance to provide service for.
        """
        self.blockchain = blockchain

    def GetBlockchainState(self, request, context):
        """
        Returns the current state of the blockchain as a list of blocks.
        """
        blockchain_data = []
        for block in self.blockchain.chain:
            blockchain_data.append(pb2.Block(
                index=block.index,
                previous_hash=block.previous_hash,
                timestamp=str(block.timestamp),
                data=block.data,
                nonce=block.nonce,
                hash=block.hash
            ))
        return pb2.BlockchainState(blocks=blockchain_data)

    def AddBlock(self, request, context):
        """
        Adds a new block to the blockchain with the provided data.
        """
        data = request.data
        self.blockchain.add_block(data)
        return pb2.BlockResponse(success=True)

# Example usage
if __name__ == "__main__":
    # Initialize the blockchain
    blockchain = Blockchain()

    # Start the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_BlockchainServicer_to_server(BlockchainService(blockchain), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server running on port 50051...")

    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)
