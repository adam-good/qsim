import dataclasses


@dataclasses.dataclass
class Channel[T]:
    values: tuple[T,...] = ()

def send[T](chnl: Channel[T], data: T) -> Channel[T]:
    return Channel(chnl.values + (data,))
    return chnl

def recv[T](chnl: Channel[T]) -> tuple[T, Channel[T]]:
    return (
        chnl.values[0],
        Channel(chnl.values[1:])
    )
