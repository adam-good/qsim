module QuDevice
include("qubit.jl")

using Random
using IterTools
using ..Qubits:
    Qubit
    reset

mutable struct QuantumDevice
    N::Int
    allocated::Int
    Q::Dict{String, Qubit}
    QuantumDevice(n::Int) = begin
        labels = random_string(GREEK, n)
        new(
            n,0,
            Dict( "|$l⟩" => Qubit("|$l⟩",0.0) for l in labels)
        )
    end
end

const GREEK = [
    'α', 'β', 'γ', 'δ', 'ϵ', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ',
    'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'ϕ', 'χ',
    'ψ', 'ω'
]
function random_string(alphabet::Vector{Char}, N::Int)
    L::Int = round(
        log(length(alphabet), N),
        RoundUp
    )
    perms = collect(subsets(alphabet, L))
    labels = [String(p) for p in perms[1:N]]
    return labels
end

function qalloc!(device::QuantumDevice)
    if device.allocated >= device.N
        throw("NO")
    end
    q = Qubit(0.0)
    device.allocated = device.allocated + 1
    return q
end

function qfree!(device::QuantumDevice, q::Qubit)
    q = nothing
    device.allocated = device.allocated - 1
end

end