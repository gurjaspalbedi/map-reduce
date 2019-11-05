# -*- coding: utf-8 -*-
import worker_pb2
import worker_pb2_grpc

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
#        response.result['hello'] = '1'
        return response
    
    def worker_reducer(self, request, context):
        count = len(request.data.keys())
        response = worker_pb2.reducer_response()
        response.data[request.data.keys()[0]] = count
        return response
    
    def ping(self, request, context):
        response = worker_pb2.ping_response()
        response.data = f"Yes I am listening at port {request.data}"
        return response