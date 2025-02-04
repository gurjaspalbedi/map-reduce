# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import worker_pb2 as worker__pb2


class WorkerStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ping = channel.unary_unary(
        '/worker_servers.grpc_packages.Worker/ping',
        request_serializer=worker__pb2.ping_request.SerializeToString,
        response_deserializer=worker__pb2.ping_response.FromString,
        )
    self.worker_map = channel.unary_unary(
        '/worker_servers.grpc_packages.Worker/worker_map',
        request_serializer=worker__pb2.mapper_request.SerializeToString,
        response_deserializer=worker__pb2.mapper_response.FromString,
        )
    self.worker_reducer = channel.unary_unary(
        '/worker_servers.grpc_packages.Worker/worker_reducer',
        request_serializer=worker__pb2.reducer_request.SerializeToString,
        response_deserializer=worker__pb2.reducer_response.FromString,
        )


class WorkerServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def ping(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def worker_map(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def worker_reducer(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_WorkerServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ping': grpc.unary_unary_rpc_method_handler(
          servicer.ping,
          request_deserializer=worker__pb2.ping_request.FromString,
          response_serializer=worker__pb2.ping_response.SerializeToString,
      ),
      'worker_map': grpc.unary_unary_rpc_method_handler(
          servicer.worker_map,
          request_deserializer=worker__pb2.mapper_request.FromString,
          response_serializer=worker__pb2.mapper_response.SerializeToString,
      ),
      'worker_reducer': grpc.unary_unary_rpc_method_handler(
          servicer.worker_reducer,
          request_deserializer=worker__pb2.reducer_request.FromString,
          response_serializer=worker__pb2.reducer_response.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'worker_servers.grpc_packages.Worker', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
