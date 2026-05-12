"""
    Quantum

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum
using ..MathUtils

export State, angle, bloch_angle, amplitude, probability

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
    KET0

The Quantum State `|0⟩ = [1,0]`
"""
const KET0 = State(1,0)

"""
    KET1

The Quantum State `|1⟩ = [0,1]`
"""
const KET1 = State(0,1)

"""
    KETPLUS

The Quantum Superposition `|+⟩ = (|0⟩ + |1⟩) / √2`
"""
const KETPLUS = (vector(KET0) + vector(KET1)) / sqrt(2)

"""
    KETMINUS

The Quantum Superposition `|-⟩ = (|0⟩ - |1⟩) / √2`
"""
const KETMINUS = (vector(KET0) - vector(KET1)) / sqrt(2)

"""
    vector(ψ, basis=ZBasis) -> Vector{Scalar}

Expand state `ψ` into the given `basis`, returning its coordinate vector.
"""
vector(ψ::State, basis::Basis=ZBasis)::Vector{Scalar} = ψ.α * basis[1] + ψ.β * basis[2]

"""
    angle(ψ) -> Angle

Return the polar angle of state `ψ`.
"""
angle(ψ::State)::Angle = polar_angle(vector(ψ))

"""
    bloch_angle(ψ) -> Angle

Return the Bloch sphere angle (twice the polar angle) of state `ψ`.
"""
bloch_angle(ψ::State)::Angle = polar_angle(vector(ψ), x -> 2 * x)

"""
    amplitude(ψ, ϕ) -> Scalar

Compute the inner product ⟨ϕ|ψ⟩ between two states.
"""
amplitude(ψ::State, ϕ::State)::Scalar = dotprod(vector(ψ), vector(ϕ))

"""
    probability(ψ, ϕ) -> Scalar

Compute the probability of measuring `ψ` in state `ϕ` via the Born rule.
"""
probability(ψ::State, ϕ::State)::Scalar = amplitude(ψ, ϕ)^2

end  # module Quantum
