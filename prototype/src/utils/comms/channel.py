import dataclasses
import queue

@dataclasses.dataclass
class Channel[T]:
    values: queue.Queue[T] = queue.Queue[T]()

    def send(self, data: T):
        self.values.put(data)

    def recv(self) -> T:
        return self.values.get()
