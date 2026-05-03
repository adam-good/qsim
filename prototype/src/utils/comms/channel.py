import dataclasses
import queue

@dataclasses.dataclass
class Channel[T]:
    transmitter: queue.Queue[T] = queue.Queue[T]()
    reciever: queue.Queue[T] = queue.Queue[T]()

    def send(self, data: T):
        self.transmitter.put(data)

    def recv(self) -> T:
        return self.reciever.get()

def compliment(channel: Channel) -> Channel:
    return Channel(channel.reciever, channel.transmitter)

def channel_pair[T]() -> tuple[Channel[T], Channel[T]]:
    channel = Channel[T]()
    return channel, compliment(channel)
