import numpy as np
from .quantum_state import QuantumState
from .qubit import Qubit

class QuantumCircuit:
    def __init__(self, num_qubits):
        self.qubits = [Qubit() for _ in range(num_qubits)]
        self.gates = []

    def add_gate(self, gate):
        self.gates.append(gate)

    def run(self):
        state_vector = np.array([1.0] + [0.0] * (2 ** len(self.qubits) - 1))
        for gate in self.gates:
            state_vector = gate(state_vector)
        return QuantumState(state_vector)
