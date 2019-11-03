# -*- coding: utf-8 -*-

import grpc

import worker_pb2_grpc
#import worker_pb2

def run(ip, port):
    channel = grpc.insecure_channel(f'{ip}:{port}')
        
    stub = worker_pb2_grpc.WorkerStub(channel)
    
    return stub
#        with open('dummy.txt', "r") as reader:
#    
#            mappers = []
#            for lines in reader.readlines():
#                mappers.append(lines)
#        request = worker_pb2.mapper_request()
#        request.lines.extend(mappers)
#        response = stub.worker_map(request)
#        print(response.result)
#    print("Greeter client received: " + response)


if __name__ == '__main__':
#    logging.basicConfig()
    run()
