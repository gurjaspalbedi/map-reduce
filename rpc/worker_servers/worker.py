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
from worker_servers.configuration import reducer_count, worker_list, inverted_index_path, word_count_path,\
word_count_map, word_count_reducer, inverted_index_map, inverted_index_reducer, mapper_tasks_path, \
reducer_task_path
import math
import os
import pickle
from data_store.server import init_data_store, connect_datastore, command_to_store
from data_store.rpc_constants import INITIAL_STAGE, \
INTERMEDIATE_STAGE, FINAL_STAGE, TASK_INVERTED_INDEX, TASK_WORD_COUNT

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
    reducer_task_count = 0
    unique_keys = set()
    for l in data:
        for item in l:
            unique_keys.add(item.key)
            combined.append((item.key, item.value))
            
    combined.sort(key = lambda x: x[0])
    print('combined', combined)
    print('unique keys', unique_keys)
    unique_keys = list(unique_keys)
    
    for key in unique_keys:
        key_wise = []
        for item in combined:
            if item[0] == key:
                key_wise.append((key, item[1]))
        
        print('_______________________')
        print(key_wise)
        print('+++++++++++++++++++++++')
        with open(f'{reducer_task_path}task{reducer_task_count}', 'wb') as task_file:    
            pickle.dump((key, key_wise), task_file)
            reducer_task_count += 1
    return reducer_task_count


def convert_to_proto_format(list_of_tuples):
    
    response_list = []
    tup = worker_pb2.tuple()
    for key,value in list_of_tuples:
        tup = worker_pb2.tuple()
        tup.key = key
        tup.value = value
        response_list.append(tup)
    return response_list
    
def run_map_red(cluster_id, task_type):
    
    global stubs
    stub_list = stubs.get(int(cluster_id), 0)
    data = run_map_chunks(cluster_id, task_type)
    reducer_task_count = combined_for_reducer(data)
    request = worker_pb2.reducer_request()
    
    reduce_func_path = word_count_reducer if task_type == TASK_WORD_COUNT else inverted_index_reducer
    with open(reduce_func_path, "rb") as f:
        request.reducer_function = f.read()
    for i in range(reducer_task_count):
        selected_reducer = (i+1) % len(worker_list)  
        with open(f'{reducer_task_path}task{i}', 'rb') as task_file:
            current_task = pickle.load(task_file)
            log.write('current_task for the reducer', current_task)
            request.result.extend(convert_to_proto_format(current_task[1]))
            result = stub_list[selected_reducer].worker_reducer(request)
    
    log.write("=====================FINAL RESULT OF MAP REDUCE========================")
    log.write(result)
    log.write("=======================================================================")
            


def create_mapper_data(path, task = TASK_WORD_COUNT):
    
    if not os.path.isfile(path) and task == TASK_WORD_COUNT:
        log.write('The provided path is not a file', 'critical')
        return -1
    elif not os.path.isdir(path) and task == TASK_INVERTED_INDEX:
        log.write('The provided path is not a directory', 'critical')
        return -1
    else:
        files = [path] if task == TASK_WORD_COUNT else [ f'{path}/{file_name}' for file_name in os.listdir(path)]
        task_count = 0
        for file in files:
            with open(file, 'r') as f:
                not_done = True
                while not_done:
                    line = f.readlines(10)
                    if len(line) > 0:
                        with open(f'{mapper_tasks_path}task{task_count}', 'wb') as task_file:
                            pickle.dump((file, line), task_file)
                        task_count +=1
                    else:
                        not_done = False
        return task_count               


def run_map_chunks(cluster_id, task_type = TASK_WORD_COUNT):
    path  = word_count_path if task_type == TASK_WORD_COUNT else inverted_index_path
    tasks_count = create_mapper_data(path, task_type)
    stub_list = stubs.get(int(cluster_id), 0)
    mapper_data = []
    for i in range(tasks_count):
        with open(f'{mapper_tasks_path}task{i}', 'rb') as task_file:
            current_task = pickle.load(task_file)
            selected_mapper = (i+1) % len(worker_list)  
            if stub_list and len(stub_list)>1:
                print(selected_mapper)
                stub = stub_list[selected_mapper]
                request = worker_pb2.mapper_request()
                log.write(f'Sending mapper task to node {selected_mapper}')
                request.file_name = current_task[0]
                func_path = word_count_map  if task_type == TASK_WORD_COUNT else inverted_index_map
                # Reading the map function for the given task
                with open(func_path, "rb") as f:
                    request.map_function = f.read()
                request.lines.extend(current_task[1])
                log.write('Making request to the mapper')
                response = stub.worker_map(request)
                result = list(response.result)
                mapper_data.append(result)
    return mapper_data
    
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
            run_map_red(0, TASK_WORD_COUNT)
        elif command == '2':
            destroy_cluster(0)
            

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    