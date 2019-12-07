# -*- coding: utf-8 -*-


import os
from worker_servers.worker import main
from dependency_manager import Dependencies
os.system('color')

log = Dependencies.log()

if __name__ == '__main__':
    log.write("===================================== BEGIN MAP REDUCE =========================================")
    log.write('Started from main in main.py', 'info')
    main()