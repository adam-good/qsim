using CairoMakie
using Random
using StatsBase
Random.seed!(8675309)

function polarToCartesian(θ::Float64, base1::Matrix, base2::Matrix)
    return cosd(θ) .* base1 + sind(θ) .* base2
end

function dot_prod(a::Matrix, b::Matrix)
    return sum(a .* b)
end

function magnitude(v::Matrix)
    return sqrt(sum(v.^2))
end

# Project vector a onto vector b
function project(a::Matrix, b::Matrix)
    return (dot_prod(a,b) / dot_prod(b,b)) .* b
end

const BASIS_VECTORS = [
    [0; 1;],
    [1; 0;],
]

struct Qubit
    label::String
    θ::Float64
    vec::Matrix
    display_vec::Matrix
    Qubit(label::String, θ::Float64) = new(label, θ,
        polarToCartesian(θ/2, BASIS_VECTORS[1], BASIS_VECTORS[2]),
        polarToCartesian(θ, BASIS_VECTORS[1], BASIS_VECTORS[2])
    )
    Qubit(θ::Float64) = Qubit("", θ)
end

import Base.hash, Base.isequal
function isequal(x::Qubit, y::Qubit)
    return x.θ ≈ y.θ
end
function hash(q::Qubit)
    return hash(q.θ,)
end

const KET_ZERO  = Qubit("|0⟩", 0.0)
const KET_ONE   = Qubit("|1⟩", 180.0)
const KET_PLUS  = Qubit("|+⟩", 90.0)
const KET_MINUS = Qubit("|-⟩", 270.0)

function calculate_measure_probability(q::Qubit, t::Qubit)
    proj = project(q.vec, t.vec)
    prob = magnitude(proj) ^ 2
    return prob
end

function negate(q::Qubit)
    if     q == KET_ZERO
        return KET_ONE
    elseif q == KET_ONE
        return KET_ZERO
    elseif q == KET_PLUS
        return KET_MINUS
    elseif q == KET_MINUS
        return KET_PLUS
    else
        return Qubit((q.θ + 180) % 360)
    end
end

function measure(q::Qubit, t::Qubit)
    p = calculate_measure_probability(q,t)
    r = rand(Float64)
    if p < r
        return t
    else
        return negate(t)
    end
end

function plot(q::Qubit)
    function plot_qubit(q::Qubit, realAxs::Axis, dispAxs::Axis; color::String)
        x = q.vec[1]
        y = q.vec[2]
        disp_x = q.display_vec[1]
        disp_y = q.display_vec[2]

        lines!(realAxs, [0.0, x], [0.0, y], label=q.label, color=color)
        text!(realAxs, x, y; text=q.label, fontsize=20)

        lines!(dispAxs, [0.0, disp_x], [0.0, disp_y], label=q.label, color=color)
        text!(dispAxs, disp_x, disp_y; text=q.label, fontsize=20)
    end

    fig = Figure(size=(1000,500))

    ax1 = Axis(fig[1,1], title="Standard Representation")
    arc!(ax1, Point2f(0), 1, -π/2, π/2)
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
    plot_qubit(q, ax1, ax2; color="red")

    return fig
end


display([
    KET_ZERO,
    KET_ONE,
    KET_PLUS,
    KET_MINUS
])

ψ = Qubit("|ψ⟩", 32.0)
f = plot(ψ)
save("output/qubit.png", f)
display(f)

sample = [measure(ψ, KET_ZERO) for i=1:100]
results = countmap(sample)
display(results)


labels = [q.label for q in collect(keys(results)) ]
values = collect(values(results))

fig = Figure()
ax = Axis(fig[1,1])
barplot!(ax,
    values,
    axis = (xticks = (1:length(labels), labels))
)
display(fig)