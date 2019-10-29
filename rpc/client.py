# -*- coding: utf-8 -*-

import grpc

# import the generated classes
import calculator_pb2
import calculator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('127.0.0.1:50051')
print('Operations you can do\n 1. set <key> <size>\n <pyaload>\n 2. get <KEY>\n')
#create a stub (client)
stub = calculator_pb2_grpc.GetSetStub(channel)

# create a valid request message
while True:
    value = input()
    number = calculator_pb2.Command(value=value)

# make the call
    response = stub.Operation(number)

# et voilà
    print(response.value)
