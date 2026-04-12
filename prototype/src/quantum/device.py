from contextlib import contextmanager
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Iterator
import quantum.state as qstate
import quantum.gate as qgate

QubitRef = int


@dataclass(frozen=True)
class Qubit:
    id: int
    state: qstate.QState = qstate.KET0


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
    def apply(self, qubit_id: int, gate: qgate.Gates) -> Qubit:
        pass

    @contextmanager
    def alloc(self) -> Iterator[Qubit]:
        qubit = self._alloc()
        try:
            yield qubit
        finally:
            self._dealloc(qubit)

    @contextmanager
    def n_alloc(self, n: int) -> Iterator[list[Qubit]]:
        qubits = self._n_alloc(n)
        try:
            yield qubits
        finally:
            for qubit in qubits:
                self._dealloc(qubit)