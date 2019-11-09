# -*- coding: utf-8 -*-


import os
from worker_servers.worker import main
from map_reduce_logging.logger import log
os.system('color')


if __name__ == '__main__':
    log.write("=====================================BEGIN MAP REDUCE =========================================")
    log.write('Started from main in main.py', 'info')
    main()

