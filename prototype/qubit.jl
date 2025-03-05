module Qubits

using CairoMakie
using Distributions
using StatsBase
# Random.seed!(8675309)

export Qubit

function polarToCartesian(θ::Real, base1::Vector{<:Real}, base2::Vector{<:Real})
    return cosd(θ) * base1 + sind(θ) * base2
end

function dot_prod(a::Vector{<:Real}, b::Vector{<:Real})
    return a' * b
end

function magnitude(v::Vector{<:Real})
    return sqrt(sum(v.^2))
end

# Project vector a onto vector b
function project(a::Vector{<:Real}, b::Vector{<:Real})
    return (dot_prod(a,b) / dot_prod(b,b)) .* b
end

const BASIS_VECTORS = [
    [1.0; 0.0;],
    [0.0; 1.0;],
]

struct Qubit
    label::String
    θ::Real
    vec::Vector{Real}
    display_vec::Vector{Real}
    Qubit(label::String, θ::Real) = new(label, θ,
        polarToCartesian(θ/2, BASIS_VECTORS[1], BASIS_VECTORS[2]),
        polarToCartesian(θ, BASIS_VECTORS[1], BASIS_VECTORS[2])
    )
    Qubit(θ::Real) = Qubit("", θ)
    Qubit(label::String, state::Vector{<:Real}) = begin
        θᵤ = acosd(state[1]) * 2
        θᵥ = asind(state[2]) * 2
        # I think I'm getting ahead of myself.
        # Once we're working with complex Qubits
        # The different axis reflections should work better
        # For now I think I'll just defuaut to one of the thetas
        # if θᵤ ≈ θᵥ
        #     return new(
        #         label, θᵤ, state,
        #         polarToCartesian(θᵤ, BASIS_VECTORS[1], BASIS_VECTORS[2])
        #     )
        # else
        #     throw("Invalid matrix representation: $(θᵤ) and $(θᵥ)")
        # end
        return new(
            label, θᵥ, state,
            polarToCartesian(θᵥ, BASIS_VECTORS[1], BASIS_VECTORS[2])
        )
    end
    Qubit(state::Vector{<:Real}) = Qubit("", state)
end

import Base.hash, Base.isequal
function isequal(x::Qubit, y::Qubit)
    return x.θ ≈ y.θ
end
function hash(q::Qubit)
    return hash(q.θ,)
end

const KET_ZERO  = Qubit("|0⟩", 0.0)
const KET_PLUS  = Qubit("|+⟩", 90.0)
const KET_ONE   = Qubit("|1⟩", 180.0)
const KET_MINUS = Qubit("|-⟩", -90.0)

function calculate_measure_probability(ψ::Qubit, t::Qubit)
    proj = project(ψ.vec, t.vec)
    prob = magnitude(proj) ^ 2
    return prob
end

function measure(ψ::Qubit, t::Qubit)
    p = calculate_measure_probability(ψ,t)
    r = rand(Uniform(0.0, 1.0))
    if p > r
        return t
    else
        return negate(t)
    end
end

function qplot(Ψ::Vector{Qubit})
    function plot_qubit(ψ::Qubit, realAxs::Axis, dispAxs::Axis; color::String)
        x = ψ.vec[1]
        y = ψ.vec[2]
        disp_x = ψ.display_vec[1]
        disp_y = ψ.display_vec[2]

        lines!(realAxs, [0.0, x], [0.0, y], label=ψ.label, color=color)
        text!(realAxs, x, y; text=ψ.label, fontsize=20)

        lines!(dispAxs, [0.0, disp_x], [0.0, disp_y], label=ψ.label, color=color)
        text!(dispAxs, disp_x, disp_y; text=ψ.label, fontsize=20)
    end

    fig = Figure(size=(1000,500))

    ax1 = Axis(fig[1,1], title="Standard Representation")
    arc!(ax1, Point2f(0), 1, π/2, -π/2)
    xlims!(ax1, -1.0, 1.2)
    ylims!(ax1, -1.2, 1.2)
    
    ax2 = Axis(fig[1,2], title="Bolch Circle")
    arc!(ax2, Point2f(0), 1, -π, π)
    xlims!(ax2, -1.2, 1.2)
    ylims!(ax2, -1.2, 1.2)


    plot_qubit(KET_ZERO, ax1, ax2; color="blue")
    plot_qubit(KET_ONE, ax1, ax2;  color="blue")
    plot_qubit(KET_PLUS, ax1, ax2; color="blue")
    plot_qubit(KET_MINUS, ax1, ax2; color="blue")
    for ψ in Ψ
        plot_qubit(ψ, ax1, ax2; color="red")
    end

    return fig
end

function plot_prob_dist(ψ::Qubit,t::Qubit)
    p = calculate_measure_probability(ψ,t)
    nt = negate(t)

    f = Figure()
    ax = Axis(
        f[1,1],
        xticks = (1:2, [t.label, nt.label]),
        title="Measurement Probability Distribution"
    )
    barplot!(ax, [p, 1-p])
    return f
end

end