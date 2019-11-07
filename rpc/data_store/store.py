# -*- coding: utf-8 -*-

from data_store import rpc_constants
from data_store.database import Database

db = Database()

def store_data(key, value):
#        SET OPERATION
        # Assuming that the operation will not fail
        try:
            db.set_value(key,value)
            print("STORED\r\n")
            return f"STORED KEY:{key} Value:{value}"
        except:
            # Operation failed
            print("NOT-STORED")
            print("KEY: ", key)
            print("VALUE: ", value)
            return f"NOT-STORED KEY:{key} Value:{value}"

def check_command(command):
        split_value = command.split()
#        self.wfile.write((split_value[0] + "\r\n").encode())
        if len(split_value) > 0:
            if split_value[0] == rpc_constants.GET_COMMAND:
                if len(split_value) == 2:
                    return 'get'
                else:
#                    self.wfile.write(f"GET COMMAND SHOULD BE OF FORMAT\nget <key>\r\n".encode());
                    print("GET COMMAND SHOULD BE OF FORMAT")
                    print("get <key>")
                    return rpc_constants.INVALID_GET
                
            if split_value[0] == rpc_constants.SET_COMMAND:
                if len(split_value) == 3:
                    return 'set'
                else:
#                    self.wfile.write(f"SET COMMAND SHOULD BE OF FORMAT\nset <key> <size>\n<payload>\r\n".encode());
                    print("SET COMMAND SHOULD BE OF FORMAT")
                    print("set <key> <value>")
                    return rpc_constants.INVALID_SET
            else:
                return rpc_constants.INVALID_COMMAND
        else:
            return rpc_constants.INVALID_COMMAND

def operation(command_line):
    operation = "none"
    first = command_line
    value = ""
    command = check_command(first)
    if command != rpc_constants.INVALID_COMMAND:
        
        if command == rpc_constants.SET_COMMAND:
            operation, key, value = first.split()
#            print('Waiting for payload from ' + self.thread )
#                self.wfile.write("\r\n".encode())
#                value = self.rfile.readline()
            return store_data(key, value)
            
        
        elif command == rpc_constants.GET_COMMAND:
#            print('GET OPERATION BY ' + self.thread)
            operation, key = first.split()
            value, size = db.get_value(key)
            if value:
                print("VALUE " + key+" "+size +"\n"+ value + "\nEND\r\n")
                return value
                # returning the value if it exist
#                            self.wfile.write("VALUE " + key+" "+size +"\n"+ value + "\nEND\r\n".encode(ENCODING))
#                    self.wfile.write(f"VALUE {key} {size}\r\n{value}\r\nEND\r\n".encode());
            else:
                print("KEY NOT FOUND\r\n")
                return "KEY NOT FOUND"
                # Case when key not found
#                    self.wfile.write("KEY NOT FOUND\r\n".encode())
                
    else:
        print(f"INVALID OPERATION! Command Line was {command_line}")
        return f"INVALID OPERATION! Command Line was {command_line}"