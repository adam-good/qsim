"""
    QuantumInformation

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

export QState, KET0, KET1, KETPLUS, KETMINUS

using ..CoreMath:
    ScalarUtils as Scalars,
    VectorUtils as Vectors,
    CoreMathErrors as MathErrors

include("State.jl")

using .QuantumStates: QState, KET0, KET1, KETPLUS, KETMINUS

end  # module Quantum
