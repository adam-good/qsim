"""
    QuantumInformation

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

using ..CoreMath

export QState, KET0, KET1, KETPLUS, KETMINUS

include("State.jl")

using .QuantumStates: QState, KET0, KET1, KETPLUS, KETMINUS

end  # module Quantum
