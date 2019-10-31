# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import grpc

# import the generated classes
import handler_pb2
import handler_pb2_grpc

def run():
# open a gRPC channel
    print('Initializing the command handler')
    channel = grpc.insecure_channel('127.0.0.1:50052')
    #print('Operations you can do\n 1. set <key> <size>\n <pyaload>\n 2. get <KEY>\n')
    stub = handler_pb2_grpc.WelcomeMessageServiceStub(channel)
    
    # create a valid request message
    while True:
        value = input()
        split_value = value.split()
        
        if split_value[0] == 'start_worker':
            try:
                ip = split_value[1]
                port = split_value[2]
            except:
                print("Wrong start_worker command! <start_worker> <ip> <address>")
            
            
            
            
            
        number = handler_pb2.Input(value=value)
    
    # make the call
        response = stub.init(number)
        print(f"the respoinse is {response}")
    # et voilà
        print(response.value)
