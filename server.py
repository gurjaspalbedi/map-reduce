# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 17:42:42 2019

@author: Jassi
"""
#REFERENCES
#https://realpython.com/python-csv/
#https://realpython.com/python-sockets/
#https://cs.lmu.edu/~ray/notes/pythonnetexamples/
#https://realpython.com/read-write-files-python/
#https://realpython.com/python-sockets/

import socketserver
import threading
from database import Database

db = Database()

VALID_GET = "VALID_GET"
INVALID_GET = "INVALID_GET"

VALID_SET = "VALID_SET"
INVALID_SET  = "INVALID_SET"

GET_COMMAND = "get"
SET_COMMAND = "set"

ENCODING = 'utf-8'

INVALID_COMMAND = "INVALID_COMMAND"


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class KeyValueHandler(socketserver.StreamRequestHandler):
    # Overriding the handle funtion
    # When this method is finished wfile gets flushed by itself
    
    def store_data(self, key, value, size):
#        SET OPERATION
        # Assuming that the operation will not fail
        storing_failed = False
        try:
            db.set_value(key,value, size)
        except:
            # Operation failed
            storing_failed = True
        if storing_failed:
            # Message when operation failed
            self.wfile.write("NOT-STORED\r\n".encode())
        else:
            print("Stored Data for " + self.thread)
            print("KEY: ", key)
            print("VALUE: ", value)
            # Message when operation is successful
            self.wfile.write("STORED\r\n".encode())

    def check_command(self, command):
        split_value = command.split()
#        self.wfile.write((split_value[0] + "\r\n").encode())
        if len(split_value) > 0:
            if split_value[0] == GET_COMMAND:
                if len(split_value) == 2:
                    return 'get'
                else:
                    self.wfile.write(f"GET COMMAND SHOULD BE OF FORMAT\nget <key>\r\n".encode());
                    print("GET COMMAND SHOULD BE OF FORMAT")
                    print("get <key>")
                    return INVALID_GET
            if split_value[0] == SET_COMMAND:
                if len(split_value) == 3:
                    return 'set'
                else:
                    self.wfile.write(f"SET COMMAND SHOULD BE OF FORMAT\nset <key> <size>\n<payload>\r\n".encode());
                    print("SET COMMAND SHOULD BE OF FORMAT")
                    print("set <key> <size>")
                    print("<payload>")
                    return INVALID_SET
            else:
                return INVALID_COMMAND
        else:
            return INVALID_COMMAND
        

    def handle(self):
        self.thread = threading.current_thread().getName()
        print(f'Client connected on thread:' + self.thread)
        while True:
            while True:
                operation = "none"
                first = self.rfile.readline()
                value = ""
                command = self.check_command(first.decode(ENCODING))
                if command != INVALID_COMMAND:
                    
                    if command == SET_COMMAND:
                        operation, key, size = first.decode(ENCODING).split()
                        print('Waiting for payload from ' + self.thread )
                        self.wfile.write("\r\n".encode())
                        value = self.rfile.readline()
                        self.store_data(key, value.decode(ENCODING), size)
                        break
                    
                    elif command == GET_COMMAND:
                        print('GET OPERATION BY ' + self.thread)
                        operation, key = first.decode(ENCODING).split()
                        value, size = db.get_value(key)
                        if value:
                            # returning the value if it exist
#                            self.wfile.write("VALUE " + key+" "+size +"\n"+ value + "\nEND\r\n".encode(ENCODING))
                            self.wfile.write(f"VALUE {key} {size}\r\n{value}\r\nEND\r\n".encode());
                        else:
                            # Case when key not found
                            self.wfile.write("KEY NOT FOUND\r\n".encode())
                            break
                else:
                    print("INVALID OPERATION BY " + self.thread)
                    self.wfile.write("COMMAND FORMAT NOT CORRECT\r\n".encode())
                    break
                
            # this will only be empty if the client disconnects, empty string will also be appended with '\n'
            # hence this would work even if the client sends the empty string
            # it breaks the loop if client disconnects
            if not first:
                break
        
        print("Client closed on thread" + self.thread)
        
with ThreadedTCPServer(('localhost', 9899), KeyValueHandler) as server:
    print('Waiting for the clients')
    server.serve_forever()