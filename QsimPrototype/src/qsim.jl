module QSim

include("quantum_state.jl")
include("qubit.jl")
include("gate.jl")
include("quantum_device.jl")

using .Qubits:
    Qubit,
    measure,
    qreset,
    qplot,
    plot_prob_dist,
    KET_ZERO,
    KET_ONE,
    KET_PLUS,
    KET_MINUS,
    Z_BASIS,
    X_BASIS

export Qubit,negate, measure, qplot, plot_prob_dist
export KET_ZERO, KET_ONE, KET_PLUS, KET_MINUS, Z_BASIS, X_BASIS

using .QuGates:
    hadamard,
    HADAMARD_GATE,
    H,
    not,
    NOT_GATE,
    X

export hadamard, not
export HADAMARD_GATE, H, NOT_GATE, X

using .QuDevice:
    QuantumDevice,
    qalloc!,
    qfree!
export QuantumDevice, qalloc!, qfree!

end