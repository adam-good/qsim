module Quantum
using ..MathUtils

export State

struct State
    vector::Vector{Scalar}

    function State(vector::Vector)
        vector = convert(Vector{Scalar}, vector)
        if born_rule_constraint(vector)
            return new(vector)
        else
            throw(DomainError("$vector does not satisfy Born Rule"))
        end
    end
end

Base.show(io::IO, x::State) = print(io,"|$(angle(x))⟩")

angle(ψ::State)::Angle          = angle2d(ψ.vector)
bloch_angle(ψ::State)::Angle    = angle2d(ψ.vector, x -> 2*x)

amplitude(ψ::State, ω::State)::Scalar   = dotprod(ψ.vector, ω.vector)
probability(ψ::State, ω::State)::Scalar = amplitude(ψ,ω) ^ 2


end # module Quantum
