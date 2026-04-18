import dataclasses
import typing

@dataclasses.dataclass
class Channel[T]:
    values: tuple[T,...]


def _new_channel[T]() -> Channel:
    return Channel(values=())


def _send[T](channel: Channel[T], data: T) -> Channel[T]:
    return Channel(
        values=channel.values + (data,)
    )

def _recv[T](channel: Channel[T]) -> tuple[T, Channel[T]]:
    return (
        channel.values[0],
        Channel(
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

