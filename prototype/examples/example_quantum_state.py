# prototype/examples/example_quantum_state.py

from prototype.quantum.qubit import Qubit
from prototype.quantum.quantum_state import QuantumState
import numpy as np

def main():
    # Create a custom quantum state |ψ⟩ = (1/√2)|0> + (1/√2)|1>
    state_vector = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    custom_state = QuantumState(state_vector)

    # Create a qubit with the custom state
    qubit = Qubit(custom_state)

    # Measure the qubit
    outcome = qubit.measure()
    print("Measurement Outcome:", outcome)

if __name__ == "__main__":
    main()
