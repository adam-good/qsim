"""
    Quantum

Quantum mechanics primitives: states, bases, and measurement operations.
"""
module Quantum

using ..MathUtils

export State, Basis, vector, state_angle, bloch_angle, amplitude, probability

export ZBasis, XBasis, KET0, KET1, KETPLUS, KETMINUS

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

Base.show(io::IO, x::State) = print(io, "|$(state_angle(x))⟩")

"""
    KET0

The Quantum State `|0⟩ = [1,0]`
"""
const KET0 = State(1, 0)

"""
    KET1

The Quantum State `|1⟩ = [0,1]`
"""
const KET1 = State(0, 1)

"""
    KETPLUS

The Quantum Superposition `|+⟩ = (|0⟩ + |1⟩) / √2`
"""
const KETPLUS = State(1 / sqrt(2), 1 / sqrt(2))

"""
    KETMINUS

The Quantum Superposition `|-⟩ = (|0⟩ - |1⟩) / √2`
"""
const KETMINUS = State(1 / sqrt(2), -1 / sqrt(2))

"""
    Basis

Represents an orthonormal basis for a quantum Hilbert space.
Each element is a state vector in `Vector{Scalar}` form.
"""
struct Basis
    vectors::NTuple{2,Vector{Scalar}}

    function Basis(a::Vector, b::Vector)
        return Basis((Vector{Scalar}(a), Vector{Scalar}(b)))
    end

    function Basis(vecs::NTuple{2,Vector{Scalar}})
        return new(vecs)
    end
end

Base.getindex(basis::Basis, idx) = basis.vectors[idx]

"""
    ZBasis

The computational (Z) basis: `|0⟩ = [1, 0]` and `|1⟩ = [0, 1]`.
"""
const ZBasis = Basis([1.0, 0.0], [0.0, 1.0])

"""
    XBasis

The computational (X) basis: `|+⟩ = [1/√2, 1/√2]` and `|-⟩ = [1/√2,-1/√2]`
"""
const XBasis = Basis([1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), -1 / sqrt(2)])

"""
    vector(ψ, basis=ZBasis) -> Vector{Scalar}

Expand state `ψ` into the given `basis`, returning its coordinate vector.
"""
function vector(ψ::State, basis::Basis=ZBasis)::Vector{Scalar}
    return ψ.α * basis[1] + ψ.β * basis[2]
end

"""
    state_angle(ψ) -> Angle

Return the polar angle of state `ψ`.
"""
function state_angle(ψ::State)::Angle
    return polar_angle(vector(ψ))
end

"""
    bloch_angle(ψ) -> Angle

Return the Bloch sphere angle (twice the polar angle) of state `ψ`.
"""
function bloch_angle(ψ::State)::Angle
    return polar_angle(vector(ψ), x -> 2 * x)
end

"""
    amplitude(ψ, ϕ) -> Scalar

Compute the inner product ⟨ϕ|ψ⟩ between two states.
"""
function amplitude(ψ::State, ϕ::State)::Scalar
    return dotprod(vector(ψ), vector(ϕ))
end

"""
    probability(ψ, ϕ) -> Scalar

Compute the probability of measuring `ψ` in state `ϕ` via the Born rule.
"""
function probability(ψ::State, ϕ::State)::Scalar
    return amplitude(ψ, ϕ)^2
end

end  # module Quantum
