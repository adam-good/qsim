

function polarToCartesian(θ::Float64, base1::Matrix, base2::Matrix)
    return cosd(θ/2) .* base1 + sind(θ/2) .* base2
end

const BASIS_VECTORS = [
    [0 1],
    [1 0],
]

struct Qubit
    θ::Float64
    vec::Matrix
    Qubit(θ::Float64) = new(θ, 
        polarToCartesian(θ, BASIS_VECTORS[1], BASIS_VECTORS[2])
    )
end


const KET_ZERO  = Qubit(0.0)
const KET_ONE   = Qubit(180.0)
const KET_PLUS  = Qubit(90.0)
const KET_MINUS = Qubit(270.0)

display([
    KET_ZERO,
    KET_ONE,
    KET_PLUS,
    KET_MINUS
])