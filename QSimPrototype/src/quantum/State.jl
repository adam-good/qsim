module Quantum
using ..Utils: Scalar, SatisfiesBornRule, angle2d

export State

struct State
    vector::Vector{Scalar}

    function State(vector::Vector)
        vector = convert(Vector{Scalar}, vector)
        if SatisfiesBornRule(vector)
            return new(vector)
        else
            throw(DomainError("$vector does not satisfy Born Rule"))
        end
    end
end

to_angle(ψ::State) = angle2d(ψ.vector)
to_bloch_angle(ψ::State) = angle2d(ψ.vector, x -> 2*x)

end # module Quantum
