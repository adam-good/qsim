module Utils

Scalar = AbstractFloat # NOTE: This will be updated to Complex later

function SatisfiesBornRule(w::Vector)::Bool
    return sum(x^2 for x in w) == 1.0
end

end
