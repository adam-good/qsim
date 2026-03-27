# prototype/examples/example_quantum_state.py

import math
import quantum.state as qstate
import quantum.simulation as qsim

def main():
    # Create a custom quantum state |ψ⟩ = (1/√2)|0> + (1/√2)|1>
    state_vector = (1/math.sqrt(2), 1/math.sqrt(2))
    custom_state = qstate.QState(state_vector)

    # Create a qubit with the custom state
    qubit = qsim.SimQubit(custom_state)

    # Measure the qubit
    qubit, outcome = qubit.measure(qstate.Z_BASIS)
    print(f"Measurement Outcome: {outcome}")
    print(f"Post-Measurment State: {qubit}")

if __name__ == "__main__":
    main()
