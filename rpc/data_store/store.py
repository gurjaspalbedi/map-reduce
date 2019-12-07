# -*- coding: utf-8 -*-

from data_store import rpc_constants
from data_store.database import Database
from data_store.dependency_manager import Dependencies

log = Dependencies.log()
db = Database()

def store_data(key, value, stage):
        try:
            db.set_value(key,value, stage)
            log.write(f"Sucessfully Store data with key:{key}\r\n")
            return '1'
        except:
            # Operation failed
            log.write("Unable to store the data with key {key}", 'critical')
            return '-1'

def operation(command_line, stage):
    operation = "none"
    first = command_line
    value = ""
    command = 'set' if first.startswith('set') else 'get'
    if command != rpc_constants.INVALID_COMMAND:
        
        if command == rpc_constants.SET_COMMAND:
            operation, key, value = first.split(" ", 2)
            return store_data(key, value, stage)
        
        elif command == rpc_constants.GET_COMMAND:
            operation, key = first.split()
            value, size = db.get_value(key, stage)
            if value:
                return '0'
            else:
                log.write("KEY NOT FOUND\r\n", 'critical')
                return '-2'
    else:
        log.write(f"INVALID OPERATION! Command Line was {command_line}", 'error')
        return '-1'