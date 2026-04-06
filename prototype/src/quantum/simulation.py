from dataclasses import dataclass
import quantum.device as qdev
import quantum.state as qstate
import quantum.gate as qgate


@dataclass(frozen=True, eq=False)
class SimQubit(qdev.Qubit):
    ref_id: int = 0
    state: qstate.QState = qstate.KET0

    def reset(self) -> SimQubit:
        return SimQubit(self.ref_id, qstate.KET0)

    def measure(self, basis: tuple[qstate.QState, qstate.QState]) -> tuple[SimQubit, qstate.QState]:
        collapsed = qstate.collapse(basis, self.state)
        return (SimQubit(self.ref_id, collapsed), collapsed)

    def hadamard(self) -> SimQubit:
        return SimQubit(self.ref_id, qgate.hadamard(self.state))

    def negate(self) -> SimQubit:
        return SimQubit(self.ref_id, qgate.negate(self.state))

    def ref_eq(self, other: qdev.Qubit) -> bool:
        return self.ref_id == other.ref_id

    def state_eq(self, state: qstate.QState) -> bool:
        return self.state == state

    def equiv(self, other: SimQubit) -> bool:
        return self.state == other.state

    def __repr__(self):
        return f"Qubit({self.ref_id}, {self.state})"


class SimDevice(qdev.QuantumDevice):
    def __init__(self, qubits: list[SimQubit]):
        self.qubits: dict[int, qdev.Qubit] =  {qubit.ref_id : qubit for qubit in qubits}
        self.alloc_tracker: dict[int, bool] = {qubit.ref_id : False for qubit in qubits}

    def n_available_qubits(self) -> int:
        return len([x for x in self.alloc_tracker.values() if not x])

    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        assert n <= self.n_available_qubits()
        available_qubits: list[int] = [
            i for i, is_alloc
            in self.alloc_tracker.items()
            if not is_alloc
        ]
        selection: list[int] = available_qubits[:n]
        qubits: list[qdev.Qubit] = [self.qubits[i] for i in selection]
        self.alloc_tracker.update([(i, True) for i in selection])
        return qubits

    def _alloc(self) -> qdev.Qubit:
        return self._n_alloc(1)[0]

    def _dealloc(self, qubit: qdev.Qubit):
        self.alloc_tracker[qubit.ref_id] = False
        self.qubits[qubit.ref_id] = qubit
