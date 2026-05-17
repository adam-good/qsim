"""
   VectorUtils 

Submodule of MathUtils to define a Vector Space V for QSim
V: (ℂ², +, ⋅)
ℂ² : {(x,y) | x,y ∈ ℂ}
+  : (x₁, y₁) + (x₂, y₂) = (x₁+x₂, y₁+y₂)
⋅  : c ⋅ (x, y) = (c⋅x, c⋅y)
"""
module VectorUtils

using ..Angles: Angle

export Vector2D, polar_angle, magnitude, is_normalized

"""
    Vector2D

Vector of the set ℂ² = {(x,y) | x,y ∈ ℂ}
"""
struct Vector2D <: AbstractVector{Complex}
    _x::Complex
    _y::Complex

    Vector2D(v::Vector) = begin
        if length(v) != 2
            error("Vector2D must be 2 dimensional")
        end
        return Vector2D(v[1], v[2]) 
    end
    Vector2D(x, y) = return new(complex(x), complex(y))
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
Base.:(+)(w::Vector2D, v::Vector2D) = Vector2D(vec_x(w)+vec_x(v), vec_y(w)+vec_y(v))
Base.:(*)(c::Complex, w::Vector2D) = Vector2D(c * w.x, c * w.y)

"""
    vec_x(w) -> Scalar

Returns the x element of w
"""
vec_x(w::Vector2D)::Complex = w._x

"""
    vec_y(w) -> Scalar

Returns the y element of w
"""
vec_y(w::Vector2D)::Complex = w._y

"""
    polar_angle(w, transform) -> Angle

Compute the 2D angle of vector `w` from the positive x-axis, in degrees,
after applying `transform` to the raw angle.
"""
polar_angle(w::AbstractVector, transform::Function)::Angle = polar_angle(Vector2D(w), transform)
polar_angle(w::AbstractVector)::Angle = polar_angle(w, identity)
polar_angle(w::Vector2D, transform::Function)::Angle = begin
    x = real(vec_x(w))
    y = real(vec_y(w))
    return Angle(transform(atand(y,x)))
end

"""
    magnitude(w) -> real

Compute the magnitude of w
"""
magnitude(w::AbstractVector)::Real = sum(x^2 for x in w)

"""
   is_normalized(w) -> bool

Checks whether vector is normalized, meaning it has a magnitude of 1
"""
is_normalized(w::AbstractVector) = magnitude(w) ≈ 1.0

end # module Vector2D