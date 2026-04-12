from contextlib import contextmanager
from typing import Iterator
from abc import ABCMeta, abstractmethod
import quantum.state as qstate

# TODO: Implement Device Transfer of Qubit Ownership


class Qubit(metaclass=ABCMeta):
    @property
    @abstractmethod
    def ref_id(self) -> int:
        pass

    @abstractmethod
    def copy(self) -> Qubit:
        pass

    @abstractmethod
    def measure(
        self, basis: tuple[qstate.QState, qstate.QState]
    ) -> tuple[Qubit, qstate.QState]:
        pass

    @abstractmethod
    def reset(self) -> Qubit:
        pass

    @abstractmethod
    def hadamard(self) -> Qubit:
        pass

    @abstractmethod
    def negate(self) -> Qubit:
        pass


class QuantumDevice(metaclass=ABCMeta):
    @abstractmethod
    def n_available_qubits(self) -> int:
        pass

    @abstractmethod
    def copy(self, qubit: Qubit) -> Qubit:
        pass

    @abstractmethod
    def pop_qubit(self, qubit: Qubit) -> Qubit:
        pass

    @abstractmethod
    def push_qubit(self, qubit: Qubit):
        pass

    @abstractmethod
    def transfer(self, device: QuantumDevice, qubit: Qubit):
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
            self._dealloc(qubit.reset())

    @contextmanager
    def n_alloc(self, n: int) -> Iterator[list[Qubit]]:
        qubits = self._n_alloc(n)
        try:
            yield qubits
        finally:
            for qubit in qubits:
                self._dealloc(qubit.reset())
