"""
    QSim

A Julia library for quantum state simulation. Serves as a prototype for
a more concrete implementation.
"""
module QSim

export Quantum, MathUtils
include("quantum/Quantum.jl")
using .Quantum
using .Quantum: MathUtils

end  # module QSim
