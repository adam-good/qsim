import dataclasses
import typing

@dataclasses.dataclass
class Queue[T]:
    values: tuple[T,...]


def _new_channel[T]() -> Queue:
    return Queue(values=())


def _send[T](channel: Queue[T], data: T) -> Queue[T]:
    return Queue(
        values=channel.values + (data,)
    )

def _recv[T](channel: Queue[T]) -> tuple[T, Queue[T]]:
    return (
        channel.values[0],
        Queue(
            channel.values[1:]
        )
    )

class Runtime:
    def __init__(self):
        self._tasks: list[typing.Callable] = []

    def schedule(self, fn: typing.Callable):
        self._tasks.append(fn)

    def run(self):
        while self._tasks:
            task: typing.Callable = self._tasks.pop(0)
            task()

