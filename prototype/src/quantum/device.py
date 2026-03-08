from decorator import contextmanager
from abc import ABCMeta, abstractmethod
import quantum.state as qstate

class Qubit(metaclass=ABCMeta):
    @abstractmethod
    def measure(self) -> tuple[Qubit, qstate.state]:
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def hadamard(self) -> Qubit:
        pass

    @abstractmethod
    def negate(self) -> Qubit:
        pass

class QuantumDevice(metaclass=ABCMeta):
    @abstractmethod
    def _alloc(self) -> Qubit:
        pass

    @abstractmethod
    def _dealloc(self, psi: Qubit) -> Qubit:
        pass

    @contextmanager
    def alloc(self):
        qubit = self._alloc()
        try:
            yield qubit
        finally:
            qubit.reset()
            self._dealloc(qubit)

