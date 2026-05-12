"""
    MathUtils

Mathematical utilities for quantum simulation.
Provides geometric primitives, constraints, and linear algebra helpers.
"""
module MathUtils

export Scalar, Angle, vec_x, vec_y, polar_angle, dotprod, born_rule_constraint

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
    born_rule_constraint(w) -> Bool

Check whether a vector satisfies the Born rule: the sum of squared magnitudes equals 1.
"""
born_rule_constraint(w::Vector)::Bool = sum(x^2 for x in w) ≈ 1.0

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
polar_angle(w::Vector)::Angle = polar_angle(convert(Vector{Scalar}, w), identity)
polar_angle(w::Vector, transform::Function)::Angle = polar_angle(convert(Vector{Scalar}, w), transform)
polar_angle(w::Vector{Scalar}, transform::Function)::Angle = transform(atand(vec_y(w), vec_x(w)))

"""
    dotprod(w, v) -> Scalar

Compute the Euclidean (conjugate) dot product of vectors `w` and `v`.
"""
dotprod(w::Vector, v::Vector)::Scalar = sum(w .* v)

end  # module MathUtils
