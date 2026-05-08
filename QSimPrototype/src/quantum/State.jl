module Quantum
using ..Utils: Scalar, SatisfiesBornRule

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

end # module Quantum
