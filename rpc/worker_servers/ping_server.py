# -*- coding: utf-8 -*-

import grpc

import worker_pb2_grpc
import worker_pb2

def run(port):
    with grpc.insecure_channel(f'127.0.0.1:{port}') as channel:

        stub = worker_pb2_grpc.WorkerStub(channel)
        request = worker_pb2.ping_request(data=port)
        response = stub.ping(request)
        print(response.data)
#    print("Greeter client received: " + response)


if __name__ == '__main__':
    port = input('Enter the port you want to ping on localhost')
    run(port)
