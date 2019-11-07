# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 13:19:41 2019

@author: gurjaspal
"""
#REFERENCES
#https://realpython.com/python-csv/
#https://realpython.com/python-sockets/
#https://cs.lmu.edu/~ray/notes/pythonnetexamples/
#https://realpython.com/read-write-files-python/
#https://realpython.com/python-sockets/
import csv


class Database:
    
    def __init__(self):
        self.db_path = "database.csv"
        
#        Start with empty file if the Database is reinitialized
        with open(self.db_path, "w+"):
            pass
        
        self.file = open(self.db_path, "r+")
        fieldnames = ['key', 'value', 'size']

        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames)
        self.writer.writeheader()
        self.reader = csv.DictReader(self.file)
            
    def set_value(self, key, value, size=1024):       
        self.writer.writerow({'key':key, 'value': value, 'size': size})
        self.file.flush()
        
        
    def get_value(self, key):
        with open(self.db_path) as f:
            reader = csv.DictReader(f)
            for row in reversed(list(reader)):
                if row['key'] == key:
                    return row['value'], row['size']
        return None, None