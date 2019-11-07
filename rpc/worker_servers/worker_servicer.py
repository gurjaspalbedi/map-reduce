# -*- coding: utf-8 -*-
import worker_pb2
import worker_pb2_grpc
import collections

class WokerServicer(worker_pb2_grpc.WorkerServicer):
    
    def worker_map(self, request, context):
        word_list = []
        for line in request.lines:
            for word in line.split():
                word_list.append((word, '1'))

        print('insider worker map')
        response = worker_pb2.mapper_response()
        reponse_list = []
        tup = worker_pb2.tuple()
        for key,value in word_list:
            tup = worker_pb2.tuple()
            tup.key = key
            tup.value = value
            reponse_list.append(tup)
        response.result.extend(reponse_list)
        return response
    
    def worker_reducer(self, request, context):

        response = worker_pb2.reducer_response()
        py_counter = collections.defaultdict(int)
        for tup in request.result:
            py_counter[tup.key] += 1
        
        for value, key in py_counter.items():
            response.result.add(key = str(value), value= str(key))
        return response
    
    def ping(self, request, context):
        response = worker_pb2.ping_response()
        response.data = f"Yes I am listening on port {request.data}"
        return response