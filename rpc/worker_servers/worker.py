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
from worker_servicer import WokerServicer 
from configuration import reducer_count, worker_list
import math
import itertools

clusters = collections.defaultdict(list)
threads = collections.defaultdict(list)
stubs = collections.defaultdict(list)


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

def filter_by_keys(tup, key_sequence):
    def seq_filter(tup):
        if tup[0] in key_sequence:
            return True
        else:
            return False
    return seq_filter
    
    
def combined_for_reducer(data):
    combined = []
    reducer_data = []
    unique_keys = set()
    for l in data:
        for item in l:
            unique_keys.add(item.key)
            combined.append((item.key, item.value))
            
    combined.sort(key = lambda x: x[0])
    unique_keys = list(unique_keys)
    divisions = math.ceil(len(unique_keys) / reducer_count)
    print('unique keys', len(unique_keys))
    print('divisions', divisions)
    i=0
    for r in range(reducer_count):
        try:
            reducer_keys = unique_keys[i:i+divisions]
        except:
            reducer_keys = unique_keys[i:]   
        i += divisions
        
        func = filter_by_keys(combined, reducer_keys)
        reducer_data.append(list(filter(func, combined)))
    
    print('reducer data lenght', len(reducer_data))
    return reducer_data
    
    
def run_map_red(cluster_id):
    
    global stubs
    stub_list = stubs.get(int(cluster_id), 0)
    data = run_map(cluster_id)
    for_reducer = combined_for_reducer(data)
    
    for t in range(len(for_reducer)):
        stub_list[-t-1].worker_reducer(for_reducer[t])
        
            
        

    
    
def run_map(cluster_id):
    mapper_output = []
    
    print('inside map red running', cluster_id)
    global stubs, threads
    stub_list = stubs.get(int(cluster_id), 0)
    if stub_list and len(stub_list)>1:
        r = read_lines()
        lines = r.readlines()
        divide_among = (len(threads[0]) - reducer_count)
        print(f'Number of mappers we have {divide_among}')
        print(f'Number of Reducers {reducer_count}')
        if divide_among:
            seek = math.ceil(len(lines) / divide_among)
            print(f'seek {seek}')
            i = 0
            count = 1
            for stub in stub_list[:-reducer_count]:
                print(f'Data to mapper{count}')
                count += 1
                try:
                    mappers = lines[i:i+seek]
                except:
                    mappers = lines[i:]
                i += seek
                request = worker_pb2.mapper_request()
                request.lines.extend(mappers)
                response = stub.worker_map(request)
                result = list(response.result)
                mapper_output.append(result)
                print(result)
        else:
            print(f'Nodes in cluster count not enough')
            print(f'Total nodes initialized: {len(stub_list)}')
            print(f'Reducers Count {reducer_count}')
            raise Exception('Number of initialized nodes are not correct')
            result = -1
    return mapper_output
    
            
        
#        stub_list[-1].worker_reducer()
    
           
if __name__ == '__main__':
    
    command_init = 'init_cluster('
    command_destory = 'destory('
    command_run = 'run('
    while True:
        print(repr(worker_list))
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
            init_cluster(worker_list)
            
                
        
    
#    serve()
          
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    