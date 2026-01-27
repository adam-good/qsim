# prototype/examples/example_qubit_measurement.py

from quantum.qubit import Qubit

def main():
    # Create a qubit in the initial state |0>
    qubit = Qubit()

    # Measure the qubit
    outcome = qubit.measure()
    print("Measurement Outcome:", outcome)

if __name__ == "__main__":
    main()
