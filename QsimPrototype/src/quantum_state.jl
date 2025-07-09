module QuStates

struct QuantumState
    vec::Vector{Real}

    QuantumState(α::Real, β::Real) = begin
        if abs(α)^2 + abs(β)^2 != 1
            throw("Invalid α and β")
        end
        return new(α * BASIS_VECTORS[1] + β * BASIS_VECTORS[2])
    end
end

import Base.hash, Base.isequal
function hash(q::QuantumState)
    return hash(q.vec)
end


end


