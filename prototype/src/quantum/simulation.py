from dataclasses import dataclass
import quantum.device as qdev
import quantum.state as qstate
import quantum.gate as qgate


@dataclass(frozen=True, eq=False)
class SimQubit(qdev.Qubit):
    id: int = 0  # TODO: This needs to be unique across devices
    state: qstate.QState = qstate.KET0

    @property
    def ref_id(self) -> int:
        return self.id

    def copy(self) -> qdev.Qubit:
        return SimQubit(self.id, self.state)

    def reset(self) -> SimQubit:
        return SimQubit(self.id, qstate.KET0)

    def measure(
        self, basis: tuple[qstate.QState, qstate.QState]
    ) -> tuple[SimQubit, qstate.QState]:
        collapsed = qstate.collapse(basis, self.state)
        return (SimQubit(self.id, collapsed), collapsed)

    def hadamard(self) -> SimQubit:
        return SimQubit(self.id, qgate.hadamard(self.state))

    def negate(self) -> SimQubit:
        return SimQubit(self.id, qgate.negate(self.state))

    def ref_eq(self, other: qdev.Qubit) -> bool:
        return self.id == other.ref_id

    def state_eq(self, state: qstate.QState) -> bool:
        return self.state == state

    def equiv(self, other: SimQubit) -> bool:
        return self.state == other.state

    def __repr__(self) -> str:
        return f"SimQubit({self.id}, {self.state})"


class SimDevice(qdev.QuantumDevice):
    def __init__(self, qubits: list[SimQubit]):
        self.qubits: dict[int, qdev.Qubit] = {qubit.id: qubit for qubit in qubits}
        self.allocated: set[int] = set()

    def _available(self) -> set[int]:
        return self.qubits.keys() - self.allocated

    def copy(self, qubit: qdev.Qubit) -> qdev.Qubit:
        assert qubit.ref_id in self.qubits.keys()
        return qubit.copy()

    def pop_qubit(self, qubit: qdev.Qubit) -> qdev.Qubit:
        assert qubit.ref_id in self.allocated
        qubit = self.qubits.pop(qubit.ref_id)
        self.allocated.remove(qubit.ref_id)
        return qubit

    def push_qubit(self, qubit: qdev.Qubit):
        assert qubit.ref_id not in self.qubits.keys()
        assert qubit.ref_id not in self.allocated

        self.qubits[qubit.ref_id] = qubit
        self.allocated.add(qubit.ref_id)

    def transfer(self, device: qdev.QuantumDevice, qubit: qdev.Qubit):
        qubit = self.pop_qubit(qubit)
        device.push_qubit(qubit)

    def n_available_qubits(self) -> int:
        return len(self.qubits) - len(self.allocated)

    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        assert n <= self.n_available_qubits()

        selection: list[int] = list(self._available())[:n]
        qubits: list[qdev.Qubit] = [self.qubits[i] for i in selection]
        self.allocated.update(selection)
        return qubits

    def _alloc(self) -> qdev.Qubit:
        return self._n_alloc(1)[0]

    def _dealloc(self, qubit: qdev.Qubit):
        self.allocated.remove(qubit.ref_id)
        self.qubits[qubit.ref_id] = qubit
