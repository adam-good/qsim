"""
    Quantum

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

export MathUtils
export QState, KET0, KET1, KETPLUS, KETMINUS

include("math/MathUtils.jl")
include("State.jl")

using .MathUtils
using .QuantumStates: QState, KET0, KET1, KETPLUS, KETMINUS

end  # module Quantum
