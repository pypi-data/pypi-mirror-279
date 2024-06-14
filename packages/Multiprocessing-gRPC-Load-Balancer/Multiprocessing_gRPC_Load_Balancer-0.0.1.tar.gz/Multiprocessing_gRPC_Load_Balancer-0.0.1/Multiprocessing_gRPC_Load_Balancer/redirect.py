# -*- coding: utf-8 -*-
"""
@author: Vault-of-Procrastination
"""

# In[0]

from threading import Thread, Event
from socket import socket, create_connection, timeout
from socket import AF_INET6, SOCK_STREAM, SOL_SOCKET
try:
    from socket import SO_REUSEPORT, SO_REUSEADDR, SHUT_RDWR
except:
    from socket import SO_REUSEADDR, SHUT_RDWR

# In[1]

class Socket_Server_Forwarder:
    def __init__(self, port: int) -> None:
        self.socket = socket(AF_INET6, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.socket.bind(('::', port))
        self.socket.listen()
        self.socket.settimeout(1)
        
        self.stop_event = Event()
        self.server_thread = Thread(target = self._serve)
        
        self.server_ports = []
        self.init_msgs = []
    
    @classmethod
    def random_port_creation(cls, just_port: bool = False) -> tuple[socket | None, int]:
        sock = socket(AF_INET6, SOCK_STREAM)
        sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        if just_port:
            sock.close()
        return None if just_port else sock, port
    
    def add_server(self, port: int, init_msg: str | bytes, port_in_use: bool = False) -> bool:
        if isinstance(init_msg, str):
            msg = init_msg.encode()
        else:
            msg = init_msg
        
        try:
            with socket(AF_INET6, SOCK_STREAM) as s:
                val = s.connect_ex(('localhost', port))
                assert val == 0
        except:
            if val != 111 if port_in_use else True:
                return False
        self.server_ports.append(port)
        self.init_msgs.append(msg)
        return True
    
    def start(self) -> None:
        if not self.stop_event.is_set() or self.server_thread._is_stopped:
            self.server_thread.start()
    
    def _serve(self) -> None:
        try:
            while not self.stop_event.is_set():
                try:
                    client_socket, _ = self.socket.accept()
                    self._check_destination(client_socket)
                except timeout:
                    continue
        except Exception as e:
            print('Exception occurred while accepting clients:', e, flush = True)
    
    def _check_destination(self, client: socket) -> None:
        if not (data := client.recv(4096)):
            return
        for init, port in zip(self.init_msgs, self.server_ports):
            if data.startswith(init):
                server = create_connection(('localhost', port))
                break
        else:
            client.send(b'Invalid command')
            client.shutdown(SHUT_RDWR)
            client.close()
            return
        server.send(data)
        Thread(target = self._forwarding, args = (client, server), daemon = True).start()
        Thread(target = self._forwarding, args = (server, client), daemon = True).start()
    
    def _forwarding(self, source: socket, sink: socket) -> None:
        try:
            while True:
                if not (data := source.recv(4096)):
                    break
                sink.sendall(data)
        except OSError as e:
            if (e.errno != 9) or (e.errno != 104):
                print('OSError occurred during forwarding:', e, flush = True)
        except Exception as e:
            print('Error occurred during forwarding:', e, flush = True)
        finally:
            source.close()
            try:
                sink.shutdown(SHUT_RDWR)
            except:
                pass
            sink.close()
    
    def stop(self) -> None:
        if not self.stop_event.is_set():
            self.stop_event.set()
            self.server_thread.join()
            try:
                self.socket.shutdown(SHUT_RDWR)
            except:
                pass
            self.socket.close()


