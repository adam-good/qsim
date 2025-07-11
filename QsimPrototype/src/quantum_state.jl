module QuStates

const BASIS_VECTORS = [
    [1.0; 0.0;],
    [0.0; 1.0;],
]

struct QuantumState
    vec::Vector{Real}
    α::Real
    β::Real

    QuantumState(α::Real, β::Real) = begin
        if !(abs(α)^2 + abs(β)^2 ≈ 1)
            throw("Invalid α=$α and β=$β")
        end
        return new(
            α * BASIS_VECTORS[1] + β * BASIS_VECTORS[2],
            α, β
        )
    end
    QuantumState(vec::Vector{Real}) = begin
        return new(vec, vec[1], vec[2])
    end
end

const KET_ZERO_STATE = QuantumState(1.0, 0.0)
const KET_ONE_STATE  = QuantumState(0.0, 1.0)
const KET_PLUS_STATE = QuantumState(1/sqrt(2), 1/sqrt(2))
const KET_MINUS_STATE = QuantumState(1/sqrt(2), -1/sqrt(2))


Base.:(==)(a::QuantumState, b::QuantumState) = begin
    return a.vec ≈ b.vec
end
Base.hash(q::QuantumState) = begin
    return Base.hash(q.vec)
end

function bloch_vec(state::QuantumState)
    θ = (360 + 2*asind(state.vec[2])) % 360
    return [cosd(θ); sind(θ)]
end


end


