include("qsim.jl")

using .QSim
using CairoMakie
using Distributions
using StatsBase

display([
    KET_ZERO,
    KET_ONE,
    KET_PLUS,
    KET_MINUS
])

ψ = Qubit("|ψ⟩", rand(Uniform(0.0, 180.0)))
f = qplot(ψ)
save("output/qubit.png", f)
display(f)