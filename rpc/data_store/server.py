# -*- coding: utf-8 -*-
#https://www.semantics3.com/blog/a-simplified-guide-to-grpc-in-python-6c4e25f0c506/
#This was the first grpc code that I wrote with help from the above given link.

# For loggin used the following blog post
#import logging # ref: https://realpython.com/python-logging/


import grpc
from concurrent import futures
import time
from .store_packages import store_pb2
from .store_packages import store_pb2_grpc
from data_store import store
from data_store.configuration import data_store_address
from map_reduce_logging.logger import log
stub = None


class KeyValueService(store_pb2_grpc.GetSetServicer):

    def operation(self, request, context):
        log.write(f'Store request data for value: {request.value}')
        response = store_pb2.Input()
        response.value = store.operation(request.value)
        return response
 
 
def connect_datastore():
    global stub
    channel = grpc.insecure_channel(f'127.0.0.1:{data_store_address["port"]}')
    stub =  store_pb2_grpc.GetSetStub(channel)
    
def command_to_store(value):
    log.write('Making RPC call to store')
    global stub
    number = store_pb2.Input(value=value)
    response = stub.operation(number)
    return response.value

def init_data_store(cluster_id = 0):
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    
    store_pb2_grpc.add_GetSetServicer_to_server(
            KeyValueService(), server)
    
    log.write(f'Starting Data Store. Listening on port {data_store_address["port"]}.')
    server.add_insecure_port(f'[::]:{data_store_address["port"]}')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
