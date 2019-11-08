# -*- coding: utf-8 -*-

from concurrent import futures
from .grpc_packages import worker_pb2_grpc
from .grpc_packages import worker_pb2
import grpc
import time
import collections
import ast
from multiprocessing import Process
from worker_servers.client import run
from worker_servers.worker_servicer import WokerServicer 
from worker_servers.configuration import reducer_count, worker_list, input_file_path
import math
from data_store.server import init_data_store, connect_datastore, command_to_store
from data_store.rpc_constants import INITIAL_STAGE, INTERMEDIATE_STAGE, FINAL_STAGE

from map_reduce_logging.logger import log

clusters = collections.defaultdict(list)
processes = collections.defaultdict(list)
stubs = collections.defaultdict(list)
store_stub = None


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
        worker_process  = Process(target = serve, args=(port,))
        processes[cluster_id].append(worker_process)
        worker_process.start()
   
        stubs[cluster_id].append((run(ip,port)))

    log.write(f'Cluster Initialized with id {cluster_id}')

def init_store(cluster_id = 0):
    log.write('Initializing  data store')
    init_data_store(cluster_id)

def connect_store_client():
    connect_datastore()    
    

def ping_server(port, ip= '127.0.0.1'):
    try:
        with grpc.insecure_channel(f'{ip}:{port}') as channel:
            stub = worker_pb2_grpc.WorkerStub(channel)
            request = worker_pb2.ping_request(data=port)
            response = stub.ping(request)
            log.write(response.data)
    except:
        log.write(f'Unable to ping to {ip}:{port}')
        
def destroy_cluster(cluster_id):
    global processes
    log.write(f'Killing all workers in cluster {cluster_id}')
    for process in processes[cluster_id]:
        log.write(f'Killing process {process}')
        process.terminate()
        
def read_lines():
    reader = open(input_file_path, "r")
    return reader

def filter_by_keys(tup, key_sequence):
    def seq_filter(tup):
        if tup[0] in key_sequence:
            return True
        else:
            return False
    return seq_filter

def save_initial_data(key, data):
    log.write('SAVE INITIAL DATA: Trying to store initial data from mapper {key}')
    command_to_store(f'set {key} {data}', INITIAL_STAGE)
    
def save_intermediate_data(key, data):
    log.write('SAVE INITIAL DATA: Trying to store initial data from mapper {key}')
    command_to_store(f'set {key} {data}', INTERMEDIATE_STAGE)
    
def save_final_data(key, data):
    log.write('SAVE INITIAL DATA: Trying to store initial data from mapper {key}')
    command_to_store(f'set {key} {data}', FINAL_STAGE)

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


def convert_to_proto_format(list_of_tuples):
    
    response_list = []
    tup = worker_pb2.tuple()
    for key,value in list_of_tuples:
        tup = worker_pb2.tuple()
        tup.key = key
        tup.value = value
        response_list.append(tup)
#    return response
    return response_list
    
def run_map_red(cluster_id):
    
    global stubs
    stub_list = stubs.get(int(cluster_id), 0)
    data = run_map(cluster_id)
    for_reducer = combined_for_reducer(data)
    request = worker_pb2.reducer_request()
    with open('worker_servers/word_count_reducer.py', "rb") as f:
        
        request.reducer_function = f.read()
        for t in range(len(for_reducer)):
            request.result.extend(convert_to_proto_format(for_reducer[t]))
#            print(request)
            print(stub_list[-t-1].worker_reducer(request))
    
def run_map(cluster_id):
    
    mapper_output = []
    log.write('Starting map')
    
    global stubs, processes
    stub_list = stubs.get(int(cluster_id), 0)
    if stub_list and len(stub_list)>1:
        r = read_lines()
        lines = r.readlines()
        divide_among = (len(processes[0]) - reducer_count)
        log.write(f'Number of mappers we have {divide_among}')
        log.write(f'Number of Reducers {reducer_count}')
        if divide_among:
            seek = math.ceil(len(lines) / divide_among)
            i = 0
            count = 1
            log.write(f'Data divided among mapper{count} mappers')
            for stub in stub_list[:-reducer_count]:
                count += 1
                try:
                    mappers = lines[i:i+seek]
                except:
                    mappers = lines[i:]
                i += seek
                save_initial_data(f'mapper{i}', mappers)
                request = worker_pb2.mapper_request()
                request.file_name = input_file_path
                with open('worker_servers/word_count_map.py', "rb") as f:
                    request.map_function = f.read()
                request.lines.extend(mappers)
                log.write('Making request to the mapper')
                response = stub.worker_map(request)
                result = list(response.result)
                mapper_output.append(result)
                print(result)
        else:
            print(f'Nodes in cluster count not enough')
            print(f'Total nodes initialized: {len(stub_list)}')
            print(f'Reducers Count {reducer_count}')
            log.write('Number of initialized nodes are not correct', 'critical')
            result = -1
    
    return mapper_output
    
def main():
    
    global store_stub
    log.write('Starting Process for store')
    store_process = Process(target = init_store, args=(0,))
    store_process.start()
    command_init = 'init_cluster('
    command_destory = 'destory('
    command_run = 'run('
    store_stub = connect_store_client()
    while True:
        log.write(f"Nodes in cluster {repr(worker_list)}")
        command = input()
        if command.startswith(command_init):
            command = command.replace(command_init,'')
            array = ast.literal_eval(command[:-1])
            try:
                init_cluster(array)
            except:
                log.write('Not a correct init_cluster format', 'error')
        
        elif command.startswith(command_destory):
            command = command.replace(command_destory, '')
            cluster_id = command[:-1]
            try:
                destroy_cluster(cluster_id)
            except:
                log.write('Wrong command or cluster Id', 'error')
        
        elif  command.startswith(command_run):
            log.write('Detected command as run_map_reduce, starting map reduce')
            command = command.replace(command_run, '')
            cluster_id = command[:-1]
#            try:
            run_map_red(cluster_id)
#            except:
#                print('Wrong run command')
        elif command == '1':
            init_cluster(worker_list)
            run_map_red(0)
        elif command == '2':
            destroy_cluster(0)
            

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    