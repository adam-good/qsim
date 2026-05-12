"""
    QSim

A Julia library for quantum state simulation. Serves as a prototype for
a more concrete implementation.
"""
module QSim

export Quantum

include("Utils.jl")
include("quantum/State.jl")
using .Quantum

end  # module QSim
