# -*- coding: utf-8 -*-


import threading
import handler_pb2_grpc
import grpc

def start_worker(ip, port):
    
    channel = grpc.insecure_channel('{ip}:{port}')
    
    #print('Operations you can do\n 1. set <key> <size>\n <pyaload>\n 2. get <KEY>\n')
    stub = handler_pb2_grpc.WelcomeMessageServiceStub(channel)
    
    
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
    
def init_worker(ip, port):
    
    thread= threading.Thread(target = start_worker, args=(ip, port))
    thread.start()
    
    
    