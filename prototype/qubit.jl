using CairoMakie

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

function plot(q::Qubit)
    fig = Figure()
    ax = Axis(fig[1,1])
    arc!(ax, Point2f(0), 1, -π, π)
    scatter!(ax, [0.0], [0.0]; markersize=15)
    # scatter!(ax, [q.vec[1]], [q.vec[2]]; markersize=15)

    lines!(ax, [0.0, KET_ZERO.vec[1]], [0.0, KET_ZERO.vec[2]], color="blue", label="|0⟩")
    text!(ax, KET_ZERO.vec[1], KET_ZERO.vec[2]; text="|0⟩")
    lines!(ax, [0.0, KET_ONE.vec[1]], [0.0, KET_ONE.vec[2]], color="blue", label="|1⟩")
    text!(ax, KET_ONE.vec[1], KET_ONE.vec[2]; text="|1⟩")
    lines!(ax, [0.0, q.vec[1]], [0.0, q.vec[2]], color="red", label="|ψ⟩")
    text!(ax, q.vec[1], q.vec[2]; text="|ψ⟩")

    # fig[1,2] = Legend(fig, ax, "Quantum States")
    display(fig)
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

plot(KET_PLUS)