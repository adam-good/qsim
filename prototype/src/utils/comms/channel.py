import dataclasses
import queue

@dataclasses.dataclass
class Channel[T]:
    _queue: queue.Queue[T] = queue.Queue[T]()
    
    def send(self, data: T):
        self._queue.put(data)

    def recv(self) -> T:
        return self._queue.get()

@dataclasses.dataclass
class TwoWayChannel[T]:
    _transmitter: queue.Queue[T] = queue.Queue[T]()
    _reciever: queue.Queue[T] = queue.Queue[T]()

    def send(self, data: T):
        self._transmitter.put(data)

    def recieve(self) -> T:
        return self._reciever.get()

def _compliment(channel: TwoWayChannel) -> TwoWayChannel:
    return TwoWayChannel(channel._reciever, channel._transmitter)

def channel_pair[T]() -> tuple[TwoWayChannel[T], TwoWayChannel[T]]:
    channel = TwoWayChannel[T]()
    return channel, _compliment(channel)
