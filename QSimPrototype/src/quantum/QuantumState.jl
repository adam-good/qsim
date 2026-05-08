module Quantum
using ..Utils: Scalar

export QuantumState

struct QuantumState
    vector::Vector{Scalar}
end

end
