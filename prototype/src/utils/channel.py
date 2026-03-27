from queue import Queue
from typing import NamedTuple

class Channel[T](NamedTuple):
    input: Queue[T]
    output: Queue[T]
