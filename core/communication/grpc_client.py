import grpc
import core.communication.grpc_server_pb2 as pb2
import core.communication.grpc_server_pb2_grpc as pb2_grpc

class BlockchainClient:
    def __init__(self, server_address: str):
        """
        Initializes the gRPC client for communication with a blockchain node server.
        :param server_address: Address of the server to connect to (e.g., "localhost:50051").
        """
        self.server_address = server_address
        self.channel = grpc.insecure_channel(self.server_address)
        self.stub = pb2_grpc.BlockchainStub(self.channel)

    def get_blockchain_state(self):
        """
        Retrieves the current state of the blockchain from the server.
        :return: The blockchain data received from the server.
        """
        try:
            response = self.stub.GetBlockchainState(pb2.Empty())
            for block in response.blocks:
                print(f"Index: {block.index}, Previous Hash: {block.previous_hash}, "
                      f"Timestamp: {block.timestamp}, Data: {block.data}, "
                      f"Nonce: {block.nonce}, Hash: {block.hash}")
            return response.blocks
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")
            return None

    def add_block(self, data: str):
        """
        Sends a request to add a new block with the provided data.
        :param data: Data to be stored in the new block.
        """
        try:
            response = self.stub.AddBlock(pb2.BlockData(data=data))
            if response.success:
                print(f"Block added successfully with data: {data}")
            else:
                print(f"Failed to add block with data: {data}")
        except grpc.RpcError as e:
            print(f"RPC failed: {e.code()} - {e.details()}")

# Example usage
if __name__ == "__main__":
    # Initialize the gRPC client for blockchain communication
    client = BlockchainClient(server_address="localhost:50051")

    # Get the current blockchain state from the server
    print("Getting current blockchain state...")
    blockchain_state = client.get_blockchain_state()

    # Add a new block to the blockchain via the server
    print("Adding a new block to the blockchain...")
    client.add_block(data="Block added via gRPC client")
