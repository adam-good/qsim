# prototype/examples/example_quantum_circuit.py

from prototype.quantum.gate import HGate, CNOTGate
from prototype.quantum.circuit import QuantumCircuit

def main():
    # Create a quantum circuit with 2 qubits
    circuit = QuantumCircuit(2)

    # Add Hadamard gate to the first qubit
    h_gate = HGate()
    circuit.add_gate(h_gate)

    # Add CNOT gate between the first and second qubit
    cnot_gate = CNOTGate()
    circuit.add_gate(cnot_gate)

    # Run the quantum circuit
    result_state = circuit.run()

    # Print the resulting state vector
    print("Resulting State Vector:", result_state.to_vector())

if __name__ == "__main__":
    main()
