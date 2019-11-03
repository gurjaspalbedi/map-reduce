# -*- coding: utf-8 -*-
from concurrent import futures
import worker_pb2_grpc
import worker_pb2
import grpc
import time
import collections
import ast
import threading
from client import run

clusters = collections.defaultdict(list)
threads = collections.defaultdict(list)
stubs = collections.defaultdict(list)

class WokerServicer(worker_pb2_grpc.WorkerServicer):
    
    def worker_map(self, request, context):
        word_list = []
        for line in request.lines:
            for word in line.split():
                word_list.append((word, '1'))

       
        print('insider worker map')
        response = worker_pb2.mapper_response()
        reponse_list = []
        tup = worker_pb2.tuple()
        for key,value in word_list:
            tup = worker_pb2.tuple()
            tup.key = key
            tup.value = value
            reponse_list.append(tup)
        response.result.extend(reponse_list)
#        response.result['hello'] = '1'
        return response
    
    def worker_reducer(self, request, context):
        count = len(request.data.keys())
        response = worker_pb2.reducer_response()
        response.data[request.data.keys()[0]] = count
        return response
    
    def ping(self, request, context):
        response = worker_pb2.ping_response()
        response.data = f"Yes I am listening at port {request.data}"
        return response


def serve(port):
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    worker_pb2_grpc.add_WorkerServicer_to_server(WokerServicer(), server)
    
    print(f'Starting worker server. Listening on {port}.')
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

def init_cluster(addresses):
    global cluster_len, clusters, stubs
    cluster_id = len(clusters.keys())
    clusters[cluster_id].append(addresses)
    for ip, port in addresses:
        worker_thread  = threading.Thread(target = serve, args=(port,))
        threads[cluster_id].append(worker_thread)
        worker_thread.start()
   
        stubs[cluster_id].append(run(ip,port))

    print(f'Cluster Initialized with id {cluster_id}')
    
    

def kill(ip, port):
    print(f'Stopping worker at {ip}:{port}');
    
    
def destroy(cluster_id):
    global clusters
    addresses = clusters[cluster_id]
    for ip, port in addresses:
        kill(port)
        
def read_lines():
    reader = open('dummy.txt', "r")
    return reader
    
    
def run_map_red(cluster_id):
    print('inside map red running', cluster_id)
    global stubs
    print(stubs)
    stub_list = stubs.get(int(cluster_id), 0)
    if stub_list and len(stub_list)>1:
        r = read_lines()
        for stub in stub_list[:-1]:
            mappers = []
            for lines in r.readlines(10):
                mappers.append(lines)
            print('mappers_ready')
            request = worker_pb2.mapper_request()
            request.lines.extend(mappers)
            response = stub.worker_map(request)
            print(list(response.result))
        
#        stub_list[-1].worker_reducer()
    
           
if __name__ == '__main__':
    
    command_init = 'init_cluster('
    command_destory = 'destory('
    command_run = 'run('
    while True:
        print('init_cluster([(\'127.0.0.1\', 50051), (\'127.0.0.1\', 50052)])')
        command = input()
        if command.startswith(command_init):
            command = command.replace(command_init,'')
            array = ast.literal_eval(command[:-1])
            try:
                init_cluster(array)
            except:
                print('Not a correct init_cluster format')
        
        elif command.startswith(command_destory):
            command = command.replace(command_destory, '')
            cluster_id = command[:-1]
            try:
                destroy(cluster_id)
            except:
                print('Wrong command or cluster Id')
        
        elif  command.startswith(command_run):
            print('Running map red')
            command = command.replace(command_run, '')
            cluster_id = command[:-1]
#            try:
            run_map_red(cluster_id)
#            except:
#                print('Wrong run command')
        elif command == '1':
            init_cluster([('127.0.0.1', 50051), ('127.0.0.1', 50052), ('127.0.0.1', 50053)])
            
                
        
    
#    serve()
          
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    