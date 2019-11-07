# -*- coding: utf-8 -*-
#https://www.semantics3.com/blog/a-simplified-guide-to-grpc-in-python-6c4e25f0c506/
#This was the first grpc code that I wrote with help from the above given link.

# For loggin used the following blog post
#import logging # ref: https://realpython.com/python-logging/

import grpc
from concurrent import futures
import time
import store_pb2
import store_pb2_grpc
import store
from configuration import data_store_address

class KeyValueService(store_pb2_grpc.GetSetServicer):

    def operation(self, request, context):
        print(f'Client request: {request.value}')
        response = store_pb2.Input()
        response.value = store.operation(request.value)
        return response

def init_data_store(cluster_id = 0):
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    
    store_pb2_grpc.add_GetSetServicer_to_server(
            KeyValueService(), server)
    
    
    print(f'Starting server. Listening on port {data_store_address["port"]}.')
    server.add_insecure_port(f'[::]:{data_store_address["port"]}')
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
