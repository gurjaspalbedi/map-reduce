# -*- coding: utf-8 -*-


#Ref https://realpython.com/read-write-files-python/



# -*- coding: utf-8 -*-
#https://www.semantics3.com/blog/a-simplified-guide-to-grpc-in-python-6c4e25f0c506/


import grpc
from concurrent import futures
import time
import threading
from command_handler import run
#import logging # ref: https://realpython.com/python-logging/

# import the generated classes
#import handler_pb2
import handler_pb2_grpc

# create a class to define the server functions, derived from
# calculator_pb2_grpc.CalculatorServicer
class WelcomeMessageService(handler_pb2_grpc.WelcomeMessageServiceServicer):

    def init(self, request, context):
        print(f'Master Ready! Will send the input back')
        return request


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the server
handler_pb2_grpc.add_WelcomeMessageServiceServicer_to_server(
        WelcomeMessageService(), server)

# listen on port 50051
print('Starting Master. Listening on port 50052.')
server.add_insecure_port('[::]:50052')
server.start()

# -*- coding: utf-8 -*-
print("Starting command handler")
command_handler_thread  = threading.Thread(target = run)
command_handler_thread.start()
# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)

#
#file_path = sys.argv[1]
#
#
#with open(file_path, "r") as reader:
#    
#   
#    
#    mappers = []
#    for lines in itertools.islice(reader, configuration.map_servers_count):
#        # send lines to the Mapper
#        m = new Mapper(lines)
    
    
    
    
    
    







        
        
        
