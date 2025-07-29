module Qubits

using CairoMakie
using Distributions
using StatsBase
# Random.seed!(8675309)

include("utils.jl")
using .Utils:
    dot_prod,
    magnitude,
    project

using ..QuStates:
    QuantumState,
    KET_ZERO_STATE,
    KET_ONE_STATE,
    KET_PLUS_STATE,
    KET_MINUS_STATE

struct Qubit
    label::String
    state::QuantumState
    Qubit(label::String, α::Real, β::Real) = begin
        return new(
            label,
            QuantumState(α, β)
        )
    end
    Qubit(label::String, state::QuantumState) = begin
        return Qubit(label, state.α, state.β)
    end
    Qubit(label::String, θ::Real) = begin
        α = cosd(θ); β = sind(θ)
        return Qubit(label, α, β)
    end
    Qubit(label::String, ψ::Qubit) = begin
        return Qubit(label, ψ.state)
    end
end

Base.:(==)(a::Qubit, b::Qubit) = begin
    return a.state == b.state
end
Base.hash(q::Qubit) = begin
    return Base.hash(q.state)
end

const KET_ZERO  = Qubit("|0⟩", KET_ZERO_STATE)
const KET_ONE   = Qubit("|1⟩", KET_ONE_STATE)
const KET_PLUS  = Qubit("|+⟩", KET_PLUS_STATE)
const KET_MINUS = Qubit("|-⟩", KET_MINUS_STATE)

function calculate_measure_probability(ψ::Qubit, t::QuantumState)
    proj = project(ψ.state.vec, t.vec)
    prob = magnitude(proj) ^ 2
    return prob
end

function measure(ψ::Qubit, target_state::QuantumState)
    p = calculate_measure_probability(ψ,target_state)
    r = rand(Uniform(0.0, 1.0))
    if p > r
        return Qubit(ψ.label, target_state)
    else
        # TODO: Target State should have an axis so we can just grab 
        #       the oppisite state from that
        # new_state = [target_state[2]; target_state[1];]
        new_state = QuantumState(target_state.β, target_state.α)
        return Qubit(ψ.label, new_state)
    end
end

function measure(ψ::Qubit, target_qubit::Qubit)
    return measure(ψ, target_qubit.state)
end

# TODO: The plotting functionality can also be seperated
function qplot(Ψ::Vector{Qubit})
    function plot_qubit(ψ::Qubit, realAxs::Axis, dispAxs::Axis; color::String)
        x,y = ψ.state.vec
        disp_x,disp_y = ψ.state.bloch_vec

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

function qreset(ψ::Qubit)
    return Qubit(ψ.label, 1.0, 0.0)
end

end