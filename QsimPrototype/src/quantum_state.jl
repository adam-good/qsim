module QuStates

const BASIS_VECTORS = [
    [1.0; 0.0;],
    [0.0; 1.0;],
]

struct QuantumState
    α::Real
    β::Real
    vec::Vector{Real}
    θ::Real
    bloch_vec::Vector{Real}

    QuantumState(α::Real, β::Real) = begin
        if !(abs(α)^2 + abs(β)^2 ≈ 1)
            throw("Invalid α=$α and β=$β")
        end
        θ = (360 + atand(β / α)) % 360
        bloch_θ = 2*θ
        bloch_vec = [cosd(bloch_θ); sind(bloch_θ);]
        return new(α, β, [α; β;], θ, bloch_vec)
    end
    QuantumState(vec::Vector{Real}) = begin
        return QuantumState(vec[1], vec[2])
    end
end

const KET_ZERO_STATE = QuantumState(1.0, 0.0)
const KET_ONE_STATE  = QuantumState(0.0, 1.0)
const KET_PLUS_STATE = QuantumState(1/sqrt(2), 1/sqrt(2))
const KET_MINUS_STATE = QuantumState(1/sqrt(2), -1/sqrt(2))

Base.:(==)(a::QuantumState, b::QuantumState) = begin
    return get_vec(a) ≈ get_vec(b)
end
Base.hash(q::QuantumState) = begin
    return Base.hash(q.vec)
end

end


