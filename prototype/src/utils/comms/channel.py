import dataclasses
import queue

@dataclasses.dataclass
class Channel[T]:
    _queue: queue.Queue[T] = queue.Queue[T]()
    
    def send(self, data: T):
        self._queue.put(data)

    def recv(self) -> T:
        return self._queue.get()
