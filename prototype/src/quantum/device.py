import contextlib
import typing
import dataclasses as dcls
import quantum.state as qstate
import quantum.gate as qgate

@dcls.dataclass
class Qubit:
    id: int = 0
    state: qstate.QState = qstate.KET0

    @property
    def ref_id(self) -> int:
        return self.id

    def __repr__(self) -> str:
        return f"SimQubit({self.id}, {self.state})"


class QuantumDevice:
    def __init__(self, qubits: list[Qubit]):
        self.qubits: dict[int, Qubit] = {qubit.id: qubit for qubit in qubits}
        self.allocated: set[int] = set()

    def _available(self) -> set[int]:
        return self.qubits.keys() - self.allocated

    def n_available_qubits(self) -> int:
        return len(self.qubits) - len(self.allocated)

    def _n_alloc(self, n: int) -> list[Qubit]:
        assert n <= self.n_available_qubits()

        selection: list[int] = list(self._available())[:n]
        qubits: list[Qubit] = [self.qubits[i] for i in selection]
        self.allocated.update(selection)
        return qubits

    def _alloc(self) -> Qubit:
        return self._n_alloc(1)[0]

    def _dealloc(self, qubit: Qubit):
        self.allocated.remove(qubit.ref_id)
        self.qubits[qubit.ref_id] = qubit

    @contextlib.contextmanager
    def alloc(self, n: int) -> typing.Iterator[list[Qubit]]:
        qubits = self._n_alloc(n)
        try:
            yield qubits
        finally:
            for q in qubits:
                self._dealloc(q)
        

    @contextlib.contextmanager
    def alloc_single(self) -> typing.Iterator[Qubit]:
        qubit = self._alloc()
        try:
            yield qubit
        finally:
            self._dealloc(qubit)
