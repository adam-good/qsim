module QuGates
include("qubit.jl")

using LinearAlgebra: I
using ..Qubits:
    Qubit

struct Gate
    mat::Matrix{Real}
    Gate(m::Matrix) = begin
        if m' * m ≈ I
            new(m)
        else
            throw("Invalid Matrix for Gate $m")
        end
    end
end

const HADAMARD_GATE = Gate([1 1; 1 -1;] / √2)
const H = HADAMARD_GATE
const NOT_GATE = Gate([0 1; 1 0;])
const X = NOT_GATE

function hadamard(ψ::Qubit)
    ϕ::Vector{Real} = H.mat * ψ.vec
    return Qubit("H$(ψ.label)", ϕ)
end

function not(ψ::Qubit)
    ϕ::Vector{Real} = X.mat * ψ.vec
    return Qubit("X$(ψ.label)", ϕ)
end

end