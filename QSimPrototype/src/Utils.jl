"""
    MathUtils

Mathematical utilities for quantum simulation.
Provides geometric primitives, constraints, and linear algebra helpers.
"""
module MathUtils

export Scalar, Angle, Vector2, angle2d, dotprod, born_rule_constraint

"""
    Scalar

Abstract type for scalar values used throughout QSim.
Currently `AbstractFloat`; will be updated to `Complex` for full quantum support.
"""
const Scalar::DataType = AbstractFloat

"""
    Angle(value::Real)

Represents a planar angle in degrees, normalized to [0, 360).
"""
struct Angle
    value::Real

    function Angle(θ::Real)::Angle
        return new((θ + 360) % 360)
    end
end

Base.show(io::IO, x::Angle) = print(io, "$(x.value)°")
Base.convert(::Type{Angle}, x::Real) = Angle(x)

"""
    Vector2 <: AbstractVector{Scalar}

A 2-element vector backed by `x` and `y` fields. Implements `AbstractVector` interface
for compatibility with LinearAlgebra operations.
"""
struct Vector2 <: AbstractVector{Scalar}
    x::Scalar
    y::Scalar

    function Vector2(w::Vector)
        if length(w) != 2
            throw(ErrorException("Vector2 Must be Length 2"))
        end
        return new(w[1], w[2])
    end
end

Base.size(w::Vector2) = (2,)
Base.getindex(w::Vector2, i::Int) = begin
    if i == 1
        return w.x
    elseif i == 2
        return w.y
    else
        throw(ErrorException("Index Out of Range $i"))
    end
end
Base.getindex(w::Vector2, I::Vararg{Int, 2}) = getindex(w, I)

"""
    born_rule_constraint(w) -> Bool

Check whether a vector satisfies the Born rule: the sum of squared magnitudes equals 1.
"""
born_rule_constraint(w::Vector2)::Bool = sum(x^2 for x in w) ≈ 1.0

"""
    vec_x(w) -> Scalar

Return the first element of vector `w`.
"""
vec_x(w::Vector)::Scalar = w[1]

"""
    vec_y(w) -> Scalar

Return the second element of vector `w`.
"""
vec_y(w::Vector)::Scalar = w[2]

"""
    angle2d(w, transform)

Compute the 2D angle of vector `w` from the positive x-axis, in degrees,
after applying `transform` to the raw angle.
"""
angle2d(w::Vector)::Angle = angle2d(convert(Vector{Scalar}, w), identity)
angle2d(w::Vector, transform::Function)::Angle = angle2d(convert(Vector{Scalar}, w), transform)
angle2d(w::Vector{Scalar}, transform::Function)::Angle = transform(atand(vec_y(w), vec_x(w)))

"""
    dotprod(w, v) -> Scalar

Compute the Euclidean (conjugate) dot product of vectors `w` and `v`.
"""
dotprod(w::Vector, v::Vector)::Scalar = sum(w .* v)

end  # module MathUtils
