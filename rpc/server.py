# -*- coding: utf-8 -*-
#https://www.semantics3.com/blog/a-simplified-guide-to-grpc-in-python-6c4e25f0c506/


import grpc
from concurrent import futures
import time
#import logging # ref: https://realpython.com/python-logging/

# import the generated classes
import calculator_pb2
import calculator_pb2_grpc

# import the original calculator.py
import calculator

# create a class to define the server functions, derived from
# calculator_pb2_grpc.CalculatorServicer
class KeyValueService(calculator_pb2_grpc.GetSetServicer):

    # calculator.square_root is exposed here
    # the request and response are of the data type
    # calculator_pb2.Number
    def Operation(self, request, context):
        print('Client request: {request.value}')
        response = calculator_pb2.Operation()
        response.value = calculator.operation(request.value)
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
calculator_pb2_grpc.add_GetSetServicer_to_server(
        KeyValueService(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
