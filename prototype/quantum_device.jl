module QuDevice
include("qubit.jl")

using Random
using IterTools
using DataStructures
using ..Qubits:
    Qubit,
    qreset

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
mutable struct QuantumDevice
    num_qubits::Int
    qubits::Dict{String, Qubit}
    queue::Queue{Qubit}
    QuantumDevice(n::Int) = begin
        labels = random_string(GREEK, n)
        qubits = Dict( "|$l⟩" => Qubit("|$l⟩",0.0) for l in labels)
        queue = Queue{Qubit}(n)
        for q in values(qubits)
            enqueue!(queue, q)
        end
        new(n,qubits,queue)
    end
end

function qalloc!(device::QuantumDevice)
    q = dequeue!(device.queue)
    return q
end

function qfree!(device::QuantumDevice, q::Qubit)
    q = qreset(q)
    enqueue!(device.queue, q)
end

end