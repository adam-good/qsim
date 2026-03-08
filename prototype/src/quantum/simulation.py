from quantum.device import Qubit, QuantumDevice
import quantum.state as qstate
import quantum.gate as qgate

class SimQubit(Qubit):
    def __init__(self):
        self.reset()
    
    def reset(self) -> SimQubit:
        self.state = qstate.ket0()
        return self

    def measure(self) -> tuple[SimQubit, qstate.state]:
        self.state = qstate.collapse(self.state)
        return (self, self.state)

    def hadamard(self) -> Qubit:
        self.state = qgate.hadamard(self.state)
        return self

    def negate(self) -> Qubit:
        self.state = qgate.negate(self.state)
        return self

