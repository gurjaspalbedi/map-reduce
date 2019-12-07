# -*- coding: utf-8 -*-
import sys
sys.path.append("../rpc")
import os
from worker_servers.worker import main
from dependency_manager import Dependencies
from api.instances.main import insert_preem_machine, get_instance_details, delete_machine, terminate_machine, start_machine
import time

log = Dependencies.log()

def start_master():
    start_machine('master')

def init_cluster(cluster_id, worker_count):

    worker_details = {}
    for i in range(worker_count):
        worker_name = f'c-{cluster_id}-worker{i}'
        worker_details[worker_name] = -1
        start_machine(worker_name)
    
    while worker_count > 1:
        time.sleep(2)
        for name in [w for w in worker_details.keys() if w != -1]:
            details = get_instance_details(name)
            if details['status'] == "RUNNING":
                ip = details['networkInterfaces'][0]['networkIP']
                worker_count -= 1
                worker_details[name] = ip
                log.write(f"Instance {name} running at {ip}", 'debug')
    
    return worker_details


def destroy_cluster(clusters, cluster_id):
    nodes = clusters[cluster_id]
    log.write(f'Terminating cluster {cluster_id} Begin')
    worker_count = len(nodes)
    deleted_instances = {}
    for node in nodes:
        deleted_instances[node] = False

    for node in nodes:
        terminate_machine(node)
    
    while worker_count > 1:
        time.sleep(2)

        for name in [node for node in deleted_instances if not deleted_instances[node]]:
            details = get_instance_details(name)
            if details['status'] == "TERMINATED":
                worker_count -= 1
                deleted_instances[name] = 1
                log.write(f"Instance {name} terminated at", 'debug')
    
    return True
    
    # return worker_details

os.system('color')

if __name__ == '__main__':
    clusters = {}
    log.write("=====================================BEGIN MAP REDUCE =========================================")
    log.write('Started from main in main.py', 'info')
    log.write('Initializing Master Node')

    workers = init_cluster(1, 4)
    clusters['cluster0'] = workers
    log.write("Successfully started following instances")

    for name in workers:
        log.write(f"{name}: {workers[name]}", 'debug')

    f= 'cluster0'
    if destroy_cluster(clusters, f):
        log.write(f'Deleted all instances in cluster {f}')
        del clusters['cluster0']
    
    log.write(f'Total clusters running: {len(clusters.keys())}')
        
    # start_master()
    # master_ready = False
    # while not master_ready:
    #     time.sleep(2)
    #     details = get_instance_details('master')
    #     if details['status'] == 'RUNNING':
    #         master_ready = True
    #         log.write(f"Master node running at {details['networkInterfaces'][0]['networkIP']}", 'debug')
    #         break







