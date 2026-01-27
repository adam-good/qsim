import numpy as np

class Gate:
    def __call__(self, qubits):
        raise NotImplementedError("Subclasses must implement this method")

class HGate(Gate):
    def __call__(self, qubits):
        # Apply Hadamard gate to the qubit(s)
        h_gate = np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]])
        return h_gate @ qubits

class CNOTGate(Gate):
    def __call__(self, qubits):
        # Apply CNOT gate to the qubit(s)
        cnot_gate = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
        return cnot_gate @ qubits
