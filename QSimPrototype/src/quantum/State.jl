"""
    Quantum

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum
using ..MathUtils

export State, angle, bloch_angle, amplitude, probability

"""
    Basis

Represents an orthonormal basis for a quantum Hilbert space.
Each element is a state vector in `Vector{Scalar}` form.
"""
struct Basis
    vectors::Vector{Vector{Scalar}}

    function Basis(a::Vector, b::Vector)
        a = convert(Vector{Scalar}, a)
        b = convert(Vector{Scalar}, b)
        return Basis([a, b])
    end

    function Basis(vecs::Vector{Vector{Scalar}})
        # TODO: Check vectors are all orthogonal
        return new(vecs)
    end
end

Base.getindex(basis::Basis, idx) = basis.vectors[idx]

"""
    ZBasis

The computational (Z) basis: `|0⟩ = [1, 0]` and `|1⟩ = [0, 1]`.
"""
const ZBasis = Basis([1, 0], [0, 1])

"""
    State(α, β)

Represents a quantum state with amplitudes `α` and `β`.
Must satisfy the Born rule: |α|² + |β|² = 1.
"""
struct State
    α::Scalar
    β::Scalar

    function State(w::Vector)
        if length(w) != 2
            throw(ErrorException("Vector Must Be Size 2, Found Size $(length(w))"))
        end
        w = Vector{Scalar}(w)
        return State(w[1], w[2])
    end

    function State(α::Real, β::Real)
        α = Scalar(α)
        β = Scalar(β)
        vec = Vector([α, β])
        if born_rule_constraint(vec)
            return new(α, β)
        else
            throw(DomainError("$vec does not satisfy Born Rule"))
        end
    end
end

Base.show(io::IO, x::State) = print(io, "|$(angle(x))⟩")

"""
    vector(ψ, basis=ZBasis) -> Vector{Scalar}

Expand state `ψ` into the given `basis`, returning its coordinate vector.
"""
vector(ψ::State, basis::Basis=ZBasis)::Vector{Scalar} = ψ.α * basis[1] + ψ.β * basis[2]

"""
    angle(ψ) -> Angle

Return the polar angle of state `ψ`.
"""
angle(ψ::State)::Angle = angle2d(vector(ψ))

"""
    bloch_angle(ψ) -> Angle

Return the Bloch sphere angle (twice the polar angle) of state `ψ`.
"""
bloch_angle(ψ::State)::Angle = angle2d(vector(ψ), x -> 2 * x)

"""
    amplitude(ψ, ω) -> Scalar

Compute the inner product ⟨ψ|ω⟩ between two states.
"""
amplitude(ψ::State, ω::State)::Scalar = dotprod(vector(ψ), vector(ω))

"""
    probability(ψ, ω) -> Scalar

Compute the probability of measuring `ψ` in state `ω` via the Born rule.
"""
probability(ψ::State, ω::State)::Scalar = amplitude(ψ, ω)^2

end  # module Quantum
