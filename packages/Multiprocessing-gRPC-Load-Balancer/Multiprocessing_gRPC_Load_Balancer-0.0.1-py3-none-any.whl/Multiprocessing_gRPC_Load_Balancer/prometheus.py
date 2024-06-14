# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

from threading import Thread
from http.server import HTTPServer
from typing import Optional, Sequence, Iterable, Union
from prometheus_client import CollectorRegistry, MetricsHandler
from prometheus_client import Gauge, Counter, Enum, Histogram, Summary, Info
try:
    from socket import AF_INET6, SOL_SOCKET, SO_REUSEPORT
except:
    from socket import AF_INET6, SOL_SOCKET

__all__ = ['Prometheus_Server']

# In[1]

class Prometheus_Server(HTTPServer):
    address_family = AF_INET6
    allow_reuse_port = True
    
    def __init__(self, port: int) -> None:
        self.prometheus_register = CollectorRegistry()
        self.prometheus_handler = MetricsHandler.factory(self.prometheus_register)
        self.server_thread = Thread(target = self.serve_forever)
        super().__init__(('localhost', port), self.prometheus_handler, (start := hasattr(HTTPServer, 'allow_reuse_port')))
        if not start:
            self.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
            self.socket.bind(self.server_address)
            self.server_address = self.socket.getsockname()
            self.server_activate()
    
    def create_gauge(self, name: str, documentation: str, labelnames: Iterable[str] = (), namespace: str = '', subsystem: str = '',
                     unit: str = '', _labelvalues: Optional[Sequence[str]] = None, multiprocess_mode: str = 'all') -> Gauge:
        return Gauge(name, documentation, labelnames, namespace, subsystem, unit, self.prometheus_register, _labelvalues, multiprocess_mode)
    
    def create_counter(self, name: str, documentation: str, labelnames: Iterable[str] = (), namespace: str = '',
                       subsystem: str = '', unit: str = '', _labelvalues: Optional[Sequence[str]] = None) -> Counter:
        return Counter(name, documentation, labelnames, namespace, subsystem, unit, self.prometheus_register, _labelvalues)
    
    def create_enum(self, name: str, documentation: str, labelnames: Iterable[str] = (), namespace: str = '', subsystem: str = '',
                    unit: str = '', _labelvalues: Optional[Sequence[str]] = None, states: Optional[Sequence[str]] = None) -> Enum:
        return Enum(name, documentation, labelnames, namespace, subsystem, unit, self.prometheus_register, _labelvalues, states)
    
    def create_histogram(self, name: str, documentation: str, labelnames: Iterable[str] = (), namespace: str = '', subsystem: str = '', unit: str = '',
                         _labelvalues: Optional[Sequence[str]] = None, buckets: Sequence[Union[float, str]] = Histogram.DEFAULT_BUCKETS) -> Histogram:
        return Histogram(name, documentation, labelnames, namespace, subsystem, unit, self.prometheus_register, _labelvalues, buckets)
    
    def create_summary(self, name: str, documentation: str, labelnames: Iterable[str] = (), namespace: str = '',
                       subsystem: str = '', unit: str = '', _labelvalues: Optional[Sequence[str]] = None) -> Summary:
        return Summary(name, documentation, labelnames, namespace, subsystem, unit, self.prometheus_register, _labelvalues)
    
    def create_info(self, name: str, documentation: str, labelnames: Iterable[str] = (), namespace: str = '',
                    subsystem: str = '', unit: str = '', _labelvalues: Optional[Sequence[str]] = None) -> Info:
        return Info(name, documentation, labelnames, namespace, subsystem, unit, self.prometheus_register, _labelvalues)
    
    def start(self) -> None:
        if not (self.server_thread.is_alive() or self.server_thread._is_stopped):
            self.server_thread.start()
    
    def close(self) -> None:
        self.shutdown()
        self.server_thread.join()
        self.socket.close()


