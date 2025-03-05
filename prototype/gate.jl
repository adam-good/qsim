module QuGates
include("qubit.jl")

using ..Qubits:
    Qubit

struct Gate
    mat::Matrix{Real}
end

const HADAMARD_GATE = Gate([1 1; 1 -1;] / √2)
const H = HADAMARD_GATE

function hadamard(ψ::Qubit)
    new_state::Vector{Real} = H.mat * ψ.vec
    display(new_state)
    return Qubit("H$(ψ.label)", new_state)
end

end