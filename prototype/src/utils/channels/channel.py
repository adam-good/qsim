from abc import ABCMeta, abstractmethod

class Channel(metaclass=ABCMeta):
    @abstractmethod
    def send(self, payload: list[object]): pass
    @abstractmethod
    def recv(self) -> list[object]: pass
