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
    display_vec::Matrix
    Qubit(θ::Float64) = new(θ, 
        polarToCartesian(θ, BASIS_VECTORS[1], BASIS_VECTORS[2]),
        polarToCartesian(2*θ, BASIS_VECTORS[1], BASIS_VECTORS[2])
    )
end

function plot(q::Qubit)
    function plot_qubit(q::Qubit, realAxs::Axis, dispAxs::Axis; label::String, color::String)
        x = q.vec[1]
        y = q.vec[2]
        disp_x = q.display_vec[1]
        disp_y = q.display_vec[2]

        lines!(realAxs, [0.0, x], [0.0, y], label=label, color=color)
        text!(realAxs, x, y; text=label, fontsize=20)

        lines!(dispAxs, [0.0, disp_x], [0.0, disp_y], label=label, color=color)
        text!(dispAxs, disp_x, disp_y; text=label, fontsize=20)
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


    plot_qubit(KET_ZERO, ax1, ax2; label="|0⟩", color="blue")
    plot_qubit(KET_ONE, ax1, ax2; label="|1⟩", color="blue")
    plot_qubit(KET_PLUS, ax1, ax2; label="|+⟩", color="blue")
    plot_qubit(KET_MINUS, ax1, ax2; label="|-⟩", color="blue")
    plot_qubit(q, ax1, ax2; label="|ψ⟩", color="red")

    return fig
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

f = plot(Qubit(32.0))
save("output/qubit.png", f)
display(f)