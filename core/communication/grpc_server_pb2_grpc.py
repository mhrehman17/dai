# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import core.communication.grpc_server_pb2 as grpc__server__pb2


class BlockchainStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBlockchainState = channel.unary_unary(
                '/core.communication.Blockchain/GetBlockchainState',
                request_serializer=grpc__server__pb2.Empty.SerializeToString,
                response_deserializer=grpc__server__pb2.BlockchainState.FromString,
                )
        self.AddBlock = channel.unary_unary(
                '/core.communication.Blockchain/AddBlock',
                request_serializer=grpc__server__pb2.BlockData.SerializeToString,
                response_deserializer=grpc__server__pb2.BlockResponse.FromString,
                )


class BlockchainServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetBlockchainState(self, request, context):
        """RPC to get the current blockchain state
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddBlock(self, request, context):
        """RPC to add a new block to the blockchain
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BlockchainServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBlockchainState': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBlockchainState,
                    request_deserializer=grpc__server__pb2.Empty.FromString,
                    response_serializer=grpc__server__pb2.BlockchainState.SerializeToString,
            ),
            'AddBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.AddBlock,
                    request_deserializer=grpc__server__pb2.BlockData.FromString,
                    response_serializer=grpc__server__pb2.BlockResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'core.communication.Blockchain', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Blockchain(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetBlockchainState(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/core.communication.Blockchain/GetBlockchainState',
            grpc__server__pb2.Empty.SerializeToString,
            grpc__server__pb2.BlockchainState.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddBlock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/core.communication.Blockchain/AddBlock',
            grpc__server__pb2.BlockData.SerializeToString,
            grpc__server__pb2.BlockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
