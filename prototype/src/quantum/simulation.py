import quantum.device as qdev
import quantum.state as qstate
import quantum.gate as qgate

class SimQubit(qdev.Qubit):
    def __init__(self, ref_id: int, init_state: qstate.QState = qstate.KET0):
        self.ref_id = ref_id
        self.state = init_state
    
    def reset(self) -> SimQubit:
        self.state = qstate.reset(self.state)
        return self

    def measure(self, basis: tuple[qstate.QState, qstate.QState]) -> tuple[SimQubit, qstate.QState]:
        self.state = qstate.collapse(basis, self.state)
        return (self, self.state)

    def hadamard(self) -> SimQubit:
        self.state = qgate.hadamard(self.state)
        return self

    def negate(self) -> SimQubit:
        self.state = qgate.negate(self.state)
        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SimQubit):
            return self.state == other.state
        elif isinstance(other, qstate.QState):
            return self.state == other
        else:
            raise NotImplementedError()

    def __hash__(self):
        return hash(self.state)

    def __repr__(self):
        return f"\u007C{self.state}\u27E9"

class SimDevice(qdev.QuantumDevice):
    # TODO: Add list of qubits as parameter
    def __init__(self, qubits: list[SimQubit]):
        self.qubits: dict[int, qdev.Qubit] = {qubit.ref_id:qubit for qubit in qubits}
        self.alloc_tracker: dict[int, bool] = {qubit.ref_id:False for qubit in qubits}

    @property
    def n_qubits(self) -> int:
        return len([x for x in self.alloc_tracker.values() if not x])


    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        assert n <= self.n_qubits
        available_qubits: list[int] = [
            i for i,is_alloc
            in self.alloc_tracker.items()
            if not is_alloc
        ]
        selection: list[int] = available_qubits[:n]
        qubits: list[qdev.Qubit] = [self.qubits[i] for i in selection]
        self.alloc_tracker.update([(i,True) for i in selection])
        return qubits

    
    def _alloc(self) -> qdev.Qubit:
        return self._n_alloc(1)[0]
    
    def _dealloc(self, qubit: qdev.Qubit):
        for i in self.alloc_tracker.keys():
            if not self.alloc_tracker[i]:
                break

        self.alloc_tracker[i] = False
        self.qubits[i] = qubit
