from contextlib import contextmanager
from typing import Iterator
from abc import ABCMeta, abstractmethod
import quantum.state as qstate

class Qubit(metaclass=ABCMeta):
    @abstractmethod
    def measure(self, basis: tuple[qstate.QState, qstate.QState]) -> tuple[Qubit, qstate.QState]:
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
    @property
    @abstractmethod
    def n_qubits(self) -> int:
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

    @contextmanager
    def alloc(self) -> Iterator[Qubit]:
        qubit = self._alloc()
        try:
            yield qubit
        finally:
            qubit.reset()
            self._dealloc(qubit)

    @contextmanager
    def n_alloc(self, n: int) -> Iterator[list[Qubit]]:
        qubits = self._n_alloc(n)
        try:
            yield qubits
        finally:
            for qubit in qubits:
                qubit.reset()
                self._dealloc(qubit)
