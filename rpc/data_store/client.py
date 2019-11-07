# -*- coding: utf-8 -*-

import grpc

# import the generated classes
from .store_packages import store_pb2
from .store_pacakges import store_pb2_grpc
from configuration import data_store_address
# open a gRPC channel
channel = grpc.insecure_channel(f'127.0.0.1:{data_store_address["port"]}')
print('Operations you can do\n 1. set <key> <size>\n <pyaload>\n 2. get <KEY>\n')
#create a stub (client)
stub = store_pb2_grpc.GetSetStub(channel)

# create a valid request message
while True:
    value = input()
    number = store_pb2.Input(value=value)

# make the call
    response = stub.operation(number)

# et voilà
    print(response.value)
