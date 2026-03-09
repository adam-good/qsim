from typing import Generator
from contextlib import contextmanager
import quantum.device as qdev
import quantum.state as qstate
import quantum.gate as qgate

class SimQubit(qdev.Qubit):
    def __init__(self):
        self.reset()
    
    def reset(self) -> SimQubit:
        self.state = qstate.reset(self.state)
        return self

    def measure(self) -> tuple[SimQubit, qstate.QState]:
        self.state = qstate.collapse(self.state)
        return (self, self.state)

    def hadamard(self) -> SimQubit:
        self.state = qgate.hadamard(self.state)
        return self

    def negate(self) -> SimQubit:
        self.state = qgate.negate(self.state)
        return self

type Qubit = qdev.Qubit | SimQubit
class SimDevice(qdev.QuantumDevice):
    def __init__(self, n):
        self.qubits: dict[int, Qubit] = {i:SimQubit() for i in range(n)}
        self.alloc_tracker: dict[int, bool] = {i:False for i in range(n)}
        

    def _alloc(self) -> Qubit:
        for i in self.alloc_tracker.keys():
            if self.alloc_tracker[i]:
                break

        qubit = self.qubits[i]
        self.alloc_tracker[i] = True

        return qubit

    def _dealloc(self, psi: Qubit):
        for i in self.alloc_tracker.keys():
            if not self.alloc_tracker[i]:
                break

        self.alloc_tracker[i] = False
        self.qubits[i] = psi

    @contextmanager
    def alloc(self) -> Generator[Qubit]:
        qubit = self._alloc()
        try:
            yield qubit
        finally:
            qubit.reset()
            self._dealloc(qubit)
