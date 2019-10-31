# -*- coding: utf-8 -*-
from concurrent import futures
import worker_pb2_grpc
import worker_pb2
import grpc
import time
import collections

class WokerServicer(worker_pb2_grpc.WorkerServicer):
    
    def worker_map(self, request, context):
        word_dict = collections.defaultdict(lambda: 0)
        for line in request.lines:
            for word in line.split():
                word_dict[word] = '1'

       
        print('insider worker map')
        response = worker_pb2.mapper_response()
        for key,value in word_dict.items():
            response.result[key] = value
#        response.result['hello'] = '1'
        return response


def serve(port=50051):
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=50))
    worker_pb2_grpc.add_WorkerServicer_to_server(WokerServicer(), server)
    
    print(f'Starting worker server. Listening on {port}.')
    server.add_insecure_port('[::]:50051')
    server.start()
    
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
        
if __name__ == '__main__':
    serve()
          