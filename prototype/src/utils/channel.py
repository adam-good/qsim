import dataclasses


@dataclasses.dataclass
class Channel[T]:
    values: tuple[T,...] = ()

def send[T](chnl: Channel[T], data: T) -> Channel[T]:
    return Channel(chnl.values + (data,))
    return chnl

def recv[T](chnl: Channel[T]) -> tuple[T | None, Channel[T] | None]:
    if not chnl.values:
        return (None, None)
    return (
        chnl.values[0],
        Channel(chnl.values[1:])
    )
