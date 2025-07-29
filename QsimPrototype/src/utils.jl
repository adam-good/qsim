module Utils
# TODO: I should move some of these linear algebra functions to a utility module
function dot_prod(a::Vector{<:Real}, b::Vector{<:Real})
    return a' * b
end

function magnitude(v::Vector{<:Real})
    return sqrt(sum(v.^2))
end

# Project vector a onto vector b
function project(a::Vector{<:Real}, b::Vector{<:Real})
    return (dot_prod(a,b) / dot_prod(b,b)) .* b
end

end