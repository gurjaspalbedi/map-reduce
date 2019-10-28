# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 23:27:30 2019

@author: gurjaspal
"""

#Ref: https://www.quantstart.com/articles/Parallelising-Python-with-Threading-and-Multiprocessing
from client import mem_client
import multiprocessing
import sys

if __name__ == "__main__":
    jobs = []
    multi = True
    for i in range(0, int(sys.argv[1])):
            process = multiprocessing.Process(target=mem_client, args=(multi, False))  
            jobs.append(process)
        
    for job in jobs:
        job.start()
    
    