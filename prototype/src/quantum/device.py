import contextlib
import typing
import dataclasses as dcls
import quantum.state as qstate
import quantum.gate as qgate

# TODO: Implement Device Transfer of Qubit Ownership


@dcls.dataclass
class Qubit:
    _id: int = 0
    _state: qstate.QState = qstate.KET0

    @property
    def ref_id(self) -> int:
        return self._id

    def __repr__(self) -> str:
        return f"SimQubit({self._id}, {self._state})"


class QuantumDevice:
    def __init__(self, qubits: list[Qubit]):
        self.qubits: dict[int, Qubit] = {qubit.ref_id: qubit for qubit in qubits}
        self.allocated: set[int] = set()

    def _available(self) -> set[int]:
        return self.qubits.keys() - self.allocated

    def n_available_qubits(self) -> int:
        return len(self._available())

    def pop_qubit(self, qubit: Qubit) -> Qubit:
        if qubit.ref_id not in self.qubits.keys():
            raise ValueError(f"Attempting to Pop Foriegn Qubit: {qubit.ref_id}")
        if qubit.ref_id not in self.allocated:
            raise ValueError(f"Attempting to Pop Unallocated Qubit: {qubit.ref_id}")

        self.allocated.remove(qubit.ref_id)
        x = self.qubits.pop(qubit.ref_id)
        assert id(x) == id(qubit)
        return x

    # TODO: Need to design a way for this to be called whenever we update qubits
    def _update_qubit_register(self, qubit: Qubit):
        if qubit.ref_id not in self.qubits.keys():
            raise ValueError("Attempting Update on Foriegn Qubit")
        if qubit.ref_id not in self.allocated:
            raise ValueError("Attempting to Update Unallocated Qubit")

        self.qubits[qubit.ref_id] = qubit

    def prepare_single_qubit(self, qubit: Qubit, gate: qgate.QGate) -> Qubit:
        qubit = Qubit(qubit.ref_id, qgate.apply_gate(gate, qubit._state))
        self._update_qubit_register(qubit)
        return qubit

    def measure_single_qubit(self, qubit: Qubit, basis: qstate.QBasis) -> qstate.QState:
        state = qstate.collapse(basis, qubit._state)
        self._update_qubit_register(Qubit(qubit.ref_id, state))
        return state

    def prepare_qubits(self, qubits: list[Qubit], gate: qgate.QGate) -> list[Qubit]:
        return [self.prepare_single_qubit(qubit, gate) for qubit in qubits]

    def measure_qubits(
        self, qubits: list[Qubit], basis: qstate.QBasis
    ) -> list[qstate.QState]:
        return [self.measure_single_qubit(qubit, basis) for qubit in qubits]

    def _n_alloc(self, n: int) -> list[Qubit]:
        assert n <= self.n_available_qubits()  # TODO: Don't use asserts like this!

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
