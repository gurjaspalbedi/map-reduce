# -*- coding: utf-8 -*-

import os
from worker_servers.worker import ping_server
os.system('color')


if __name__ == '__main__':
    port = input('Enter the port you want to ping on localhost')
    ping_server(port)




