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
from worker_servers.configuration import worker_list, inverted_index_path, word_count_path,\
word_count_map, word_count_reducer, inverted_index_map, inverted_index_reducer, mapper_tasks_path, \
reducer_task_path, configuration_path, output_path
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


def serve(port, cluster_id):
    
    global clusters
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    worker_pb2_grpc.add_WorkerServicer_to_server(WokerServicer(), server)

    failed = server.add_insecure_port(f'[::]:{port}')
    if failed != 0:
        server.start()
        log.write(f'Started worker server. Listening on {port}.', 'debug')
    else:
        if cluster_id in clusters:
            del clusters[cluster_id]
        log.write(f"Failed to start server at port: {port}", 'error')
        log.write(f"Make sure it is not already running, use destroy command to destory the cluster", 'critical')

    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

def init_cluster(cluster_id = 0):
    try:
        addresses = worker_list[cluster_id]
    except:
        log.write('Cluster_Id not presend in configuration', 'critical')
        log.write(f'You can add cluster addresses at {configuration_path}', 'critical')
        log.write('Index in worker_list represents cluster_id', 'critical')
        
    global cluster_len, clusters, stubs
    clusters[cluster_id].append(addresses)
    
    for ip, port in addresses:
      
        worker_process  = Process(target = serve, args=(port, cluster_id))
        processes[cluster_id].append(worker_process)
        worker_process.start()
   
        stubs[cluster_id].append((run(ip,port)))
    
    log.write(f'Cluster Initialized with id {cluster_id}', 'debug')
        
           
    

def init_store(cluster_id = 0):
    log.write('Initializing  data store', 'debug')
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
    global processes, clusters
    
    if len(clusters[cluster_id]) == 0:
        log.write('Either there is not cluster initialized or cluster_id is wrong', 'error')
    else:
        log.write(f'Killing all workers in cluster {cluster_id}', 'debug')
        for process in processes[cluster_id]:
            log.write(f'Killing process {process}', 'debug')
            process.terminate()
        if cluster_id in clusters:
            del clusters[cluster_id]
  
        
def save_initial_data(key, data):
    log.write(f'SAVE INITIAL DATA: Trying to store initial data from mapper {key}')
    command_to_store(f'set {key} {data}', INITIAL_STAGE)
    
def save_intermediate_data(key, data):
    log.write(f'SAVE INTERMEDIATE DATA: Trying to store initial data from mapper {key}')
    command_to_store(f'set {key} {data}', INTERMEDIATE_STAGE)
    
def save_final_data(key, data):
    log.write(f'SAVE FINAL DATA: Trying to store initial data from mapper {key}')
    command_to_store(f'set {key} {data}', FINAL_STAGE)

def combined_for_reducer(data):
    log.write('Combining the data - START')
    combined = []
    reducer_task_count = 0
    unique_keys = set()
    for l in data:
        for item in l:
            unique_keys.add(item.key)
            combined.append((item.key, item.value))
            
    combined.sort(key = lambda x: x[0])
    unique_keys = list(unique_keys)
    
    for key in unique_keys:
        key_wise = []
        for item in combined:
            if item[0] == key:
                key_wise.append((key, item[1]))
        
        with open(f'{reducer_task_path}task{reducer_task_count}', 'wb') as task_file:    
            pickle.dump((key, key_wise), task_file)
            reducer_task_count += 1
    log.write('Combining the data - END')
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
    log.write("Map reduce started")
    global stubs
    stub_list = stubs.get(int(cluster_id), 0)
    data = run_map_chunks(cluster_id, task_type)
    reducer_task_count = combined_for_reducer(data)
    request = worker_pb2.reducer_request()
    
    reduce_func_path = word_count_reducer if task_type == TASK_WORD_COUNT else inverted_index_reducer
    with open(reduce_func_path, "rb") as f:
        request.reducer_function = f.read()
    log.write("Reducing - STARTED")
    for i in range(reducer_task_count):
        selected_reducer = (i+1) % len(worker_list)  
        with open(f'{reducer_task_path}task{i}', 'rb') as task_file:
            current_task = pickle.load(task_file)
#            log.write('current_task for the reducer', current_task)
            request.result.extend(convert_to_proto_format(current_task[1]))
            result = stub_list[selected_reducer].worker_reducer(request)
    
    log.write("=====================FINAL RESULT OF MAP REDUCE========================", 'debug')
    log.write(result, 'debug')
    log.write("Reducing - END")
    for tup in result.result:
        save_final_data(f'{tup.key}', f'{tup.value}')
    
    log.write("=======================================================================")
            


def create_mapper_data(path, task = TASK_WORD_COUNT, cluster_id = 0):
    
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
#                            save_intermediate_data(f'{cluster_id}:mapper_input:{task}', (file, line))
                        task_count +=1
                    else:
                        not_done = False
        return task_count               


def run_map_chunks(cluster_id, task_type = TASK_WORD_COUNT):
    log.write('Dividing data in chunks- START')
    path  = word_count_path if task_type == TASK_WORD_COUNT else inverted_index_path
    tasks_count = create_mapper_data(path, task_type, cluster_id)
    stub_list = stubs.get(int(cluster_id), 0)
    mapper_data = []
    for i in range(tasks_count):
        with open(f'{mapper_tasks_path}task{i}', 'rb') as task_file:
            current_task = pickle.load(task_file)
            selected_mapper = (i+1) % len(worker_list[cluster_id])  
            if stub_list and len(stub_list)>1:
                stub = stub_list[selected_mapper]
                request = worker_pb2.mapper_request()
#                log.write(f'Sending mapper task to node {selected_mapper}')
                request.file_name = current_task[0]
                func_path = word_count_map  if task_type == TASK_WORD_COUNT else inverted_index_map
                # Reading the map function for the given task
                with open(func_path, "rb") as f:
                    request.map_function = f.read()
                request.lines.extend(current_task[1])
#                log.write('Making request to the mapper')
                response = stub.worker_map(request)
                result = list(response.result)
                mapper_data.append(result)
#    save_initial_data(f'{cluster_id}:{task_type}', mapper_data)
    log.write('Dividing data in chunks- END')
    return mapper_data
 
def print_running_cluster():
    global clusters
    log.write(f"Running clusters", 'error')
    for cluster in clusters:
        if len(clusters[cluster]) != 0:
            log.write(f"Cluster ID:{cluster}", 'error')
def main():
    
    global store_stub
    
    log.write('Starting Process for store', 'info')
    store_process = Process(target = init_store, args=(0,))
    store_process.start()
    command_init = 'init_cluster('
    command_destory = 'destory_cluster('
    command_run = 'run_mapred('
    store_stub = connect_store_client()
    while True:
        print_running_cluster()
        log.write(f'Following Operations can be performed. Type given number or command', 'debug')
        log.write(f'1. Init Default Cluster having nodes {repr(worker_list[0])}', 'debug')
        log.write(f'2. Run Map Reduce WORD COUNT: this is same as executing run_mapred(0,0)', 'debug')
        log.write(f'3. Run Map Reduce INVERTED INDEX: this is same as executing run_mapred(0,1)', 'debug')
        log.write(f'4. Destroy Default Cluster', 'debug')
        log.write(f'OR type any of the command <init_cluster(cluster_id)>, <run_mapred(cluster_id, task_id)>, <destory_cluter(cluster_id)>', 'debug')
        log.write('============================CONFIGURATION INFO============================')
        log.write('Master configuration file path: worker_server/configuration.py')
        log.write('Data Store configuration file path: data_store/configuration.py ')
        log.write(f'Location of MAP function:')
        log.write(f'Inverted Index: {inverted_index_map}')
        log.write(f'Word Cound: {word_count_map}')
        log.write(f'\n\n')
        log.write(f'Location of REDUCER function:')
        log.write(f'Inverted Index: {inverted_index_reducer}')
        log.write(f'Word Cound: {word_count_reducer}')
        command = input()
        if command == '1':
            init_cluster(0)
        elif command == '2':
            run_map_red(0, TASK_WORD_COUNT)
        elif command == '3':
            run_map_red(0, TASK_INVERTED_INDEX)
        elif command == '4':
            destroy_cluster(0)
        elif command.startswith(command_init):
            command = command.replace(command_init,'')
            cluster_id = ast.literal_eval(command[:-1])
            
            try:
                init_cluster(cluster_id)
            except:
                log.write('Unable to initialize cluster', 'error')
                log.write('Correct example input:')
                log.write('init_cluster([("127.0.0.1", 50053), ("127.0.0.1", 50054 )])', 'debug')
        
        elif command.startswith(command_destory):
            command = command.replace(command_destory, '')
            cluster_id = command[:-1]
            try:
                destroy_cluster(int(cluster_id))
            except:
                log.write('Unable to destory cluster', 'error')
                log.write('Correct example for destory:')
                log.write('destory_cluster(0)')
        
        elif  command.startswith(command_run):

            command = command.replace(command_run, '')
            cluster_id, task_id = command[:-1].split(",")
            task = TASK_WORD_COUNT if task_id == '0' else TASK_INVERTED_INDEX
            try:
                run_map_red(int(cluster_id), task)
            except:
                log.write('Unable to run map reduce', 'error')
                log.write('Correct example for run map reduce:', 'error')
                log.write('run_mapred(0, 0) <first_argument: cluster_id> <second_argument: task_id>', 'error')
                log.write('task should be 0 for WORD_COUNT  and 1 for Inverted Index', 'error')
        else:
            log.write("Command didn't match anything", 'critical')
                
            

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    