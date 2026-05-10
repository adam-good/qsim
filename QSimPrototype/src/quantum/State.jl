module Quantum
using ..MathUtils

export State, angle, bloch_angle, amplitude, probability

struct Basis
    vectors::Vector{Vector{Scalar}} 

    function Basis(a::Vector, b::Vector)
        a = convert(Vector{Scalar}, a); b = convert(Vector{Scalar}, b);
        return Basis([a,b])
    end

    function Basis(vecs::Vector{Vector{Scalar}})
        # TODO: Check vectors are all orthoginal
        return new(vecs)
    end
end
Base.getindex(basis::Basis, idx) = basis.vectors[idx]

const ZBasis = Basis([1,0], [0,1])
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
        α = Scalar(α); β = Scalar(β)
        vec = Vector{Scalar}([α, β])
        if born_rule_constraint(vec)
            return new(α, β)
        else
            throw(DomainError("$vector does not satisfy Born Rule"))
        end
    end
end

Base.show(io::IO, x::State) = print(io,"|$(angle(x))⟩")

vector(ψ::State, basis::Basis = ZBasis)::Vector{Scalar} = ψ.α * basis[1] + ψ.β * basis[2] 
angle(ψ::State)::Angle          = angle2d(vector(ψ))
bloch_angle(ψ::State)::Angle    = angle2d( vector(ψ), x -> 2*x)

amplitude(ψ::State, ω::State)::Scalar   = dotprod(vector(ψ), vector(ω))
probability(ψ::State, ω::State)::Scalar = amplitude(ψ,ω) ^ 2


end # module Quantum
