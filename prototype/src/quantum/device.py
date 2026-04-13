from contextlib import contextmanager
from typing import Iterator
from abc import ABCMeta, abstractmethod
import quantum.state as qstate



# NOTE: These are not immutable because they're modeling real life mutable items
class Qubit(metaclass=ABCMeta):
    
    @property
    @abstractmethod
    def ref_id(self) -> int:
        pass

class QuantumDevice(metaclass=ABCMeta):
    @abstractmethod
    def n_available_qubits(self) -> int:
        pass

    @abstractmethod
    def _alloc(self) -> Qubit:
        pass

    @abstractmethod
    def _n_alloc(self, n: int) -> list[Qubit]:
        pass

    @abstractmethod
    def _dealloc(self, qubit: Qubit):
        pass

    @abstractmethod
    def measure(self, qubit: Qubit, basis: qstate.QBasis) -> qstate.QState:
        pass

    @abstractmethod
    def reset(self, qubit: Qubit) -> Qubit:
        pass

    @abstractmethod
    def hadamard(self, qubit: Qubit) -> Qubit:
        pass

    @abstractmethod
    def negate(self, qubit: Qubit) -> Qubit:
        pass

    @contextmanager
    def alloc(self) -> Iterator[Qubit]:
        qubit = self._alloc()
        try:
            yield qubit
        finally:
            self._dealloc( self.reset(qubit))

    @contextmanager
    def n_alloc(self, n: int) -> Iterator[list[Qubit]]:
        qubits = self._n_alloc(n)
        try:
            yield qubits
        finally:
            for qubit in qubits:
                self._dealloc(self.reset(qubit))
   
