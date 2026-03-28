from typing import TypeVar
from dataclasses import dataclass
from queue import Queue

@dataclass
class ChannelEndpoint[T]:
    input: Queue[T]
    output: Queue[T]

@dataclass
class Channel[T]:
    endpoint_A: ChannelEndpoint[T]
    endpoint_B: ChannelEndpoint[T]


def new_channel(chnl_type: TypeVar) -> Channel:
    queue_a = Queue[chnl_type]()
    queue_b = Queue[chnl_type]()
    endpoint_a = ChannelEndpoint(queue_a, queue_b)
    endpoint_b = ChannelEndpoint(queue_b, queue_a)
    channel = Channel[chnl_type](endpoint_a, endpoint_b)
    return channel

def get_endpoints(chnl: Channel) -> tuple[ChannelEndpoint, ChannelEndpoint]:
    return (chnl.endpoint_A, chnl.endpoint_B)

def send[T](endpoint: ChannelEndpoint[T], data: T):
    endpoint.output.put(data)

def recv[T](endpoint: ChannelEndpoint[T]) -> T:
    return endpoint.input.get()
