import threading
from dataclasses import dataclass
from queue import Queue

@dataclass
class ChannelEndpoint[T]:
    input: Queue[T]
    output: Queue[T]
    mutex: threading.Lock

@dataclass
class Channel[T]:
    endpoint_A: ChannelEndpoint[T]
    endpoint_B: ChannelEndpoint[T]

def new_channel[T]() -> Channel:
    mutex = threading.Lock()
    queue_a = Queue[T]()
    queue_b = Queue[T]()
    endpoint_a = ChannelEndpoint(queue_a, queue_b, mutex)
    endpoint_b = ChannelEndpoint(queue_b, queue_a, mutex)
    channel = Channel[T](endpoint_a, endpoint_b)
    return channel

def get_endpoints(chnl: Channel) -> tuple[ChannelEndpoint, ChannelEndpoint]:
    return (chnl.endpoint_A, chnl.endpoint_B)

def send[T](endpoint: ChannelEndpoint[T], data: T):
   endpoint.output.put(data)

def recv[T](endpoint: ChannelEndpoint[T]) -> T:
    return endpoint.input.get()
