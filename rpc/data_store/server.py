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
from data_store.dependency_manager import Dependencies
stub = None

log = Dependencies.log()
class KeyValueService(store_pb2_grpc.GetSetServicer):

    def operation(self, request, context):
        log.write(f'Data Store Operation: {request.operation}', 'debug')
        response = store_pb2.Response()
        response.data = store.operation(request.operation , request.stage)
        return response
 
 
def connect_datastore():
    global stub
    channel = grpc.insecure_channel(f'127.0.0.1:{data_store_address["port"]}')
    stub =  store_pb2_grpc.GetSetStub(channel)
    log.write('Client channel established with the store', 'info')
    
def command_to_store(value, stage):
    log.write('Making RPC call to store')
    global stub
    request = store_pb2.Request()
    request.operation = value
    request.stage = stage 
    response = stub.operation(request)
    return response.data

def init_data_store(cluster_id = 0):
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    store_pb2_grpc.add_GetSetServicer_to_server(
            KeyValueService(), server)
    
    
    failed = server.add_insecure_port(f'[::]:{data_store_address["port"]}')
    if failed != 0:
        server.start()
        log.write(f'Started Data Store. Listening on port {data_store_address["port"]}.', 'debug')
    else:
        log.write(f'Failed to start the data store', 'critical')

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
