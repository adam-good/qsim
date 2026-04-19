import dataclasses


@dataclasses.dataclass
class Channel[T]:
    values: tuple[T,...] = ()

def send[T](chnl: Channel[T], data: T) -> Channel[T]:
    chnl.values: tuple[T,...] = chnl.values + (data,)
    return chnl

def recv[T](chnl: Channel[T]) -> tuple[T, Channel[T]]:
    data: T = chnl.values[0]
    chnl.values: tuple[T,...] = chnl.values[1:]
    return data, chnl
