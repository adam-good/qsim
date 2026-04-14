# prototype/examples/example_quantum_state.py
import utils.math.vector
import math
import quantum.state as qstate


def main():
    # Create a custom quantum state |ψ⟩ = (1/√2)|0> + (1/√2)|1>
    state_vector = utils.math.vector.Vector((1 / math.sqrt(2), 1 / math.sqrt(2)))
    custom_state = qstate.QState(state_vector)

    # Collapse (such as when it is measured) quantum state
    outcome = qstate.collapse( qstate.Z_BASIS, custom_state)
    print(f"Outcome: {outcome}")


if __name__ == "__main__":
    main()
