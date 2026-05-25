"""
    QuantumInformation

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

export QState, KET0, KET1, KETPLUS, KETMINUS
export QGate

using ..CoreMath:
    ScalarUtils as Scalars,
    VectorUtils as Vectors,
    MatrixUtils as Matrices,
    CoreMathErrors as MathErrors

include("State.jl")
include("Gate.jl")

using .QuantumStates: QState, KET0, KET1, KETPLUS, KETMINUS
using .QuantumGates: QGate

end  # module Quantum
