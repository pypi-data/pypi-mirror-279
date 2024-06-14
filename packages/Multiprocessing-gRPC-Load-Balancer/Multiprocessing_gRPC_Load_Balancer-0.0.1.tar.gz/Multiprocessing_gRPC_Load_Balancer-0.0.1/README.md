# Multiprocessing_gRPC_Load_Balancer
Load Balancer for multiprocessing grpc server in **Linux**.

> [!IMPORTANT]
> The server doesn't work in Windows, this is because of a property that Linux have and Windows no.
> The *socket.REUSE_PORT*

The search for the server works in both OS.

## Installation
`pip install Multiprocessing_gRPC_Load_Balancer`

## How to use
This is a short code to show how this library works.

> [!IMPORTANT]
> If you want to share data, instances or classes between your servers, you have to handle your self.
> The gRPC class server is created on each process, but you can give arguments already initialized whit multiprocessing capabilities.

### Server
```python
import grpc, time
from typing import Iterable

from Multiprocessing_gRPC_Load_Balancer import Multiprocessing_gRPC_Load_Balancer_Server

from proto_test.Test_pb2_grpc import Test_StreamerServicer, add_Test_StreamerServicer_to_server
from proto_test.Test_pb2 import send_msg, response_msg

class Test_Server(Test_StreamerServicer):
    def __init__(self):
        pass
    
    def One_to_One(self, request: send_msg, context: grpc.ServicerContext) -> response_msg:
        print(request)
        time.sleep(1)
        return response_msg(success = True, msg = str(len(request.send)))
    
    def Many_to_One(self, request_iterator: Iterable[send_msg], context: grpc.ServicerContext) -> response_msg:
        ret = []
        for request in request_iterator:
            print(request)
            time.sleep(1)
            ret.append(request.send)
        ret.reverse()
        return response_msg(success = True, msg = ''.join(ret))
    
    def One_to_Many(self, request: send_msg, context: grpc.ServicerContext) -> Iterable[response_msg]:
        print(request)
        for data in request.send:
            time.sleep(1)
            yield response_msg(success = True, msg = str(ord(data)))
    
    def Many_to_Many(self, request_iterator: Iterable[send_msg], context: grpc.ServicerContext) -> Iterable[response_msg]:
        for request in request_iterator:
            print(request)
            time.sleep(1)
            yield response_msg(success = True, msg = str(len(request.send)))

if __name__ == '__main__':
    # this is the linux port where it would be accessible, select one that was available
    linux_port: int = 'a free port that you want to attach your server'
    
    # this is the number of process that you want to spawn
    num_of_process: int = 3
    
    # this is the number of threads each grpc process will have
    num_of_threads: int = 10
    
    # this is the weight this server will have over the other ones, more weight indicates that will be preferable to select
    num_of_weight: int = 1
    
    server = Multiprocessing_gRPC_Load_Balancer_Server(linux_port, num_of_process, num_of_threads, num_of_weight)
    
    # this is the class where that will handle the service methods, the class should be not initiated
    grpc_service_cls = Test_Server
    
    # this is the function to add the class to the server
    add_service_to_server = add_Test_StreamerServicer_to_server
    
    # this is if you want to block the code until you cancel it, or to continue running more code while the server is up, is default to True
    ## Important if you put the block arg to False you need to handle the infinite loop until you want to close it and run server.close()
    ## If you don't do this, the subprocess will continue consuming resources from your computer or server.
    block_the_code: bool = True
    
    # *args: List[Any] # is a list of arguments that you want to pass to the class onces is running on each child process
    args_for_class = []
    
    # **kwargs: Dict[str, Any] # is a dict of key value arguments that you want to pass to the class onces is running on each child process
    kwargs_for_the_class = {}
    
    server.start(grpc_service_cls, add_service_to_server, block_the_code, *args_for_class, **kwargs_for_the_class)
    
    ### This is just a way to block the code, you can use any way you want, just remember to close the server.
    if not block_the_code:
        from time import sleep
        try:
            while True:
                sleep(86400) # 86400 seconds == 1 day
        except:
            server.close() # Close the server, this safetly stop and join every thread and subprocess created
```

### Client
```python

from typing import List, Union

from proto_test.Test_pb2 import send_msg
from proto_test.Test_pb2_grpc import Test_StreamerStub

from Multiprocessing_gRPC_Load_Balancer import search_servers

class Test_Client:
    def __init__(self, servers: List[str]) -> None:
        self.servers = servers
    
    def one_to_one(self, data: str) -> List[Union[str, int]]:
        with search_servers(self.servers) as channel:
            test_stub = Test_StreamerStub(channel)
            response = test_stub.One_to_One(send_msg(send = data))
            ret = [response.success, int(response.msg)]
        return ret
    
    def many_to_one(self, data: List[str]) -> List[Union[str, int]]:
        with search_servers(self.servers) as channel:
            test_stub = Test_StreamerStub(channel)
            response = test_stub.Many_to_One(iter([send_msg(send = x) for x in data]))
            ret = [response.success, response.msg]
        return ret
    
    def one_to_many(self, data: str) -> List[List[Union[str, int]]]:
        ret = []
        with search_servers(self.servers) as channel:
            test_stub = Test_StreamerStub(channel)
            for response in test_stub.One_to_Many(send_msg(send = data)):
                ret.append([response.success, int(response.msg)])
        return ret
    
    def many_to_many(self, data: List[str]) -> List[List[Union[str, int]]]:
        ret = []
        with search_servers(self.servers) as channel:
            test_stub = Test_StreamerStub(channel)
            for response in test_stub.Many_to_Many(iter([send_msg(send = x) for x in data])):
                ret.append([response.success, int(response.msg)])
        return ret

# just need to give the class a list of host + port of the linux server
# the code will search automatically what server is with less demand and more weight
client = Test_Client(['linux_ip1:linux_port1', 'linux_ip2:linux_port2', 'linux_ip3:linux_port3'])

# one data send, one data receive
client.one_to_one('Test')

# multiple data send, one data receive
client.many_to_one([x for x in 'Test'])

# multiple data send, one data receive
client.one_to_many('Test')

# return a list of each value if complete and the lenght of the text
client.many_to_many(['x'*x for x in range(10)])
```


