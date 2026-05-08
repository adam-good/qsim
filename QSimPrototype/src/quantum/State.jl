module Quantum
using ..Utils: Scalar

export State

struct State
    vector::Vector{Scalar}
end

end
