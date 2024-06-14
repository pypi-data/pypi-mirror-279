# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

from grpc import (ServerInterceptor,
                  unary_unary_rpc_method_handler , unary_stream_rpc_method_handler,
                  stream_unary_rpc_method_handler, stream_stream_rpc_method_handler)
from multiprocessing import Queue
from multiprocessing.synchronize import Lock

__all__ = ['Requests_Interceptor']

# In[1]

class Requests_Interceptor(ServerInterceptor):
    def __init__(self, process_num: int, queue: Queue, lock: Lock) -> None:
        self.process_num = process_num
        self.queue = queue
        self.lock = lock
    
    def update(self, value: int) -> None:
        with self.lock:
            self.queue.put_nowait({'process': self.process_num, 'value': value})
    
    def method_handled(self, method, request, context, stream: bool):
        self.update(1)
        if stream:
            ret = self.return_stream(method, request, context)
        else:
            ret = method(request, context)
        self.update(-1)
        return ret
    
    def return_stream(self, method, request, context):
        for ret in method(request, context):
            yield ret
        return StopIteration
    
    def intercept_service(self, continuation, handler_call_details):
        if (handler := continuation(handler_call_details)) is None:
            return None
        for method_name in ['unary_unary', 'unary_stream', 'stream_unary', 'stream_stream']:
            if (method := getattr(handler, method_name)) != None:
                handler_factory = globals().get(f'{method_name}_rpc_method_handler')
                break
        else:
            RuntimeError("RPC handler implementation does not exist")
        
        def handle_method(request, context):
            return self.method_handled(method, request, context, handler.response_streaming)
        
        return handler_factory(handle_method, handler.request_deserializer, handler.response_serializer)


