"""
    QSim

A Julia library for quantum state simulation. Serves as a prototype for
a more concrete implementation.
"""
module QSim

export Quantum, CoreMath

include("CoreMath/CoreMath.jl")
include("Quantum/Quantum.jl")

using .CoreMath
using .Quantum

end  # module QSim
