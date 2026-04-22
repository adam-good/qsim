import dataclasses

@dataclasses.dataclass
class Channel[T]:
    values: tuple[T,...] = ()

def send[T](chnl: Channel[T], data: T) -> Channel[T]:
    return Channel(chnl.values + (data,))
    return chnl

def recv[T](chnl: Channel[T]) -> tuple[T | None, Channel[T]]:
    if not chnl.values:
        return (None, Channel())
    head = chnl.values[0]
    tail = chnl.values[1:]
    return (head, Channel(tail))
