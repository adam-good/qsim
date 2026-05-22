"""
   VectorUtils 

Submodule of MathUtils to define a Vector Space V for QSim
V: (𝕊², +, ⋅)
𝕊² : {(x,y) | x,y ∈ 𝕊}
+  : (x₁, y₁) + (x₂, y₂) = (x₁+x₂, y₁+y₂)
⋅  : c ⋅ (x, y) = (c⋅x, c⋅y)
"""
module VectorUtils

using ..ScalarUtils: Scalar, scalar
using ..Angles: Angle

export Vector2D, polar_angle, norm2, is_normalized

"""
    Vector2D

Vector of the set 𝕊² = {(x,y) | x,y ∈ 𝕊}
"""
struct Vector2D <: AbstractVector{Scalar}
    x::Scalar
    y::Scalar

    Vector2D(v::Vector) = begin
        if length(v) != 2
            error("Vector2D must be 2 dimensional")
        end
        return Vector2D(v[1], v[2]) 
    end
    Vector2D(x, y) = return new(scalar(x), scalar(y))
end
Base.size(::Vector2D) = return(2,)
Base.getindex(v::Vector2D, i::Int) = begin
    if i == 1
        return vec_x(v)
    elseif  i == 2
        return vec_y(v)
    else
        error("index $i out of range for Vector2D $v")
    end
end
Base.:(+)(w::Vector2D, v::Vector2D) = Vector2D(w.x+v.x, w.y+v.y)
Base.:(*)(c::Scalar, w::Vector2D) = Vector2D(c * w.x, c * w.y)
Base.:(==)(w::Vector2D, v::AbstractVector) = (w.x, w.y) == (v[1], v[2])

"""
    vec_x(w) -> Scalar

Returns the x element of w
"""
vec_x(w::AbstractVector) = w[1]
vec_x(w::Vector2D)::Scalar = w.x

"""
    vec_y(w) -> Scalar

Returns the y element of w
"""
vec_y(w::AbstractVector) = w[2]
vec_y(w::Vector2D)::Scalar = w.y

"""
    polar_angle(w, transform) -> Angle

Compute the 2D angle of vector `w` from the positive x-axis, in degrees,
after applying `transform` to the raw angle.
"""
polar_angle(w::AbstractVector)::Angle = polar_angle(w, identity)
polar_angle(w::AbstractVector, transform::Function)::Angle = begin
    x = vec_x(w)
    y = vec_y(w)
    return Angle(transform(atand(y,x)))
end

"""
    norm2(w) -> ??? 

Compute the norm squared |w|² 
"""
norm2(w::AbstractVector) = sum(x^2 for x in w)

"""
   is_normalized(w) -> bool

Checks whether vector is normalized, meaning it has a magnitude of 1
"""
is_normalized(w::AbstractVector)::Bool = norm2(w) ≈ 1.0

end # module Vector2D