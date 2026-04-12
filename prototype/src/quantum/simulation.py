from dataclasses import dataclass, field
import quantum.device as qdev
import quantum.gate as qgate


@dataclass(frozen=True)
class SimQubit(qdev.Qubit):
    pass


@dataclass
class SimDevice(qdev.QuantumDevice):
    qubits: dict[int, qdev.Qubit] = field(default_factory=dict)
    gates: dict[qgate.Gates, qgate.QGate] = field(default_factory=lambda: qgate.COMMON_GATES)
    allocated: set[int] = field(default_factory=set)

    def n_available_qubits(self) -> int:
        return len(self.qubits) - len(self.allocated)

    def _available(self) -> set[int]:
        return set(self.qubits.keys()) - self.allocated

    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        if n > self.n_available_qubits():
            raise Exception("Insufficient qubits available")
        selection = list(self._available())[:n]
        self.allocated.update(selection)
        return [self.qubits[i] for i in selection]

    def _alloc(self) -> qdev.Qubit:
        return self._n_alloc(1)[0]

    def _dealloc(self, qubit: qdev.Qubit):
        self.allocated.remove(qubit.id)

    def apply(self, qubit_id: int, gate: qgate.Gates) -> qdev.Qubit:
        if qubit_id not in self.qubits:
            raise Exception(f"Unknown qubit id: {qubit_id}")
        current = self.qubits[qubit_id]
        matrix = self.gates[gate]
        new_state = matrix @ current.state
        new_qubit = qdev.Qubit(qubit_id, new_state)
        self.qubits[qubit_id] = new_qubit
        return new_qubit
