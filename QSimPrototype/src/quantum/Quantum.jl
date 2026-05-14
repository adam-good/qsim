"""
    Quantum

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

export MathUtils
export State

include("math/MathUtils.jl")
include("QuantumState.jl")

using .MathUtils
using .QuantumState: State

end  # module Quantum
