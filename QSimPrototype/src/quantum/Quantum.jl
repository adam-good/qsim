"""
    Quantum

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

export MathUtils
export QState

include("math/MathUtils.jl")
include("QuantumState.jl")

using .MathUtils
using .QuantumStates: QState

end  # module Quantum
