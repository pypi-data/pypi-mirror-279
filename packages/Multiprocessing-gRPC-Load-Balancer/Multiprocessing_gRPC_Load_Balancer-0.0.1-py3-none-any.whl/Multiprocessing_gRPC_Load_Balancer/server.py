# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

from time import sleep
from copyreg import pickle
from platform import system
from types import ModuleType
from importlib import import_module
from grpc import server as create_server

from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Event, Queue, Lock, cpu_count

from Multiprocessing_gRPC_Load_Balancer.prometheus import Prometheus_Server
from Multiprocessing_gRPC_Load_Balancer.interceptor import Requests_Interceptor
from Multiprocessing_gRPC_Load_Balancer.redirect import Socket_Server_Forwarder

def _pickle_module(module):
    module_name = module.__name__
    path = getattr(module, "__file__", None)
    return _unpickle_module, (module_name, path)

def _unpickle_module(module_name, path):
    return import_module(module_name)

pickle(ModuleType, _pickle_module, _unpickle_module)

__all__ = ['Multiprocessing_gRPC_Load_Balancer_Server']

# In[1]

class Multiprocessing_gRPC_Load_Balancer_Server:
    __instance = None
    
    def __new__(cls, port: int, process_num: int, threads_num: int, weight: int = 1):
        if cls.__instance is None:
            if system() != 'Linux':
                raise SystemError('This part of the code only can run successfully in Linux systems')
            cls.__instance = super(Multiprocessing_gRPC_Load_Balancer_Server, cls).__new__(cls)
            cls.__instance._init(port, process_num, threads_num, weight)
        return cls.__instance
    
    def _init(self, port: int, process_num: int, threads_num: int, weight: int = 1):
        self.port = port
        self.process_num = min(process_num, cpu_count())
        self.threads_num = threads_num
        self.weight_num = weight
        self._process = None
        
        self._stop_event = Event()
        self._queue = Queue()
        self._lock = Lock()
        self._prometheus_thread = Thread(target = self._update_prometheus)
        
        self._grpc_socket, self._grpc_port = Socket_Server_Forwarder.random_port_creation()
        _, self._prometheus_port = Socket_Server_Forwarder.random_port_creation(True)
        self._prometheus_server = Prometheus_Server(self._prometheus_port)
        
        self._redirect_stop_event = Event()
        self._redirect_server_process = Process(target = _run_redirect_server, args = (self.port, self._redirect_stop_event,
                                                [[self._grpc_port, 'PRI * HTTP/2.0', True], [self._prometheus_port, 'GET /metrics HTTP/1.1', False]]))
        
        self.process_count = self._prometheus_server.create_gauge('process_count', 'Number of Process this server have')
        self.threads_count = self._prometheus_server.create_gauge('threads_count', 'Number of Threads each Process have', ['process'])
        self.requests = self._prometheus_server.create_gauge('requests', 'Number of requests by each process', ['process'])
        self.weight = self._prometheus_server.create_gauge('weight', 'Number of the weight this server have')
        self.process_count.set(self.process_num)
        self.weight.set(self.weight_num)
        
        for i in range(self.process_num):
            self.threads_count.labels(str(i + 1)).set(self.threads_num)
            self.requests.labels(str(i + 1)).set(0)
    
    def _update_prometheus(self):
        try:
            while (item := self._queue.get()) != StopIteration:
                self.requests.labels(str(item['process'])).inc(item['value'])
        except:
            pass
    
    def start(self, grpc_cls, add_cls_to_server, block = True, *args, **kwargs):
        if self._process == None:
            self._prometheus_server.start()
            self._redirect_server_process.start()
            self._prometheus_thread.start()
            self._process = []
            for i in range(self.process_num):
                p = Process(target = _run_server, args = (f'localhost:{self._grpc_port}', self.threads_num, self._stop_event, self._queue,
                                                          self._lock, grpc_cls, add_cls_to_server, i + 1, args, kwargs))
                p.start()
                self._process.append(p)
            if block:
                try:
                    while True:
                        sleep()
                except:
                    self.close()
    
    def close(self):
        if not self._stop_event.is_set():
            self._redirect_stop_event.set()
            self._redirect_server_process.join()
            self._stop_event.set()
            for p in self._process:
                p.join()
                p.close()
            with self._lock:
                self._queue.put(StopIteration)
            self._queue.close()
            self._prometheus_thread.join()
            self._prometheus_server.close()

# In[2]

def _run_redirect_server(port, stop_event, port_list):
    server = Socket_Server_Forwarder(port)
    for port, init_msg, in_use in port_list:
        server.add_server(port, init_msg, in_use)
    server.start()
    stop_event.wait()
    server.stop()

def _run_server(address, threads_num, event, queue, lock, grpc_cls, add_cls_to_server, process_num_id, args, kwargs):
    servicer = grpc_cls(*args, **kwargs)
    interceptor = Requests_Interceptor(process_num_id, queue, lock)
    
    server = create_server(ThreadPoolExecutor(max_workers = threads_num), interceptors = (interceptor,), options = (('grpc.so_reuseport', 1),))
    add_cls_to_server(servicer, server)
    server.add_insecure_port(address)
    server.start()
    event.wait()
    server.stop(10)
    if hasattr(servicer, 'close'):
        servicer.close()


