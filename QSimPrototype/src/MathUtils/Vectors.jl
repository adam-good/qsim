"""
   VectorUtils 

Submodule of MathUtils to define a Vector Space V for QSim
V: (ℝ², +, ⋅)
ℝ² : {(x,y) | x,y ∈ ℝ}
+  : (x₁, y₁) + (x₂, y₂) = (x₁+x₂, y₁+y₂)
⋅  : c ⋅ (x, y) = (c⋅x, c⋅y)
"""
module VectorUtils

using ..HelperTypes: Scalar
using ..Angles: Angle

export Vector2D, polar_angle

"""
    Vector2D

Vector of the set ℝ² = {(x,y) | x,y ∈ ℝ}
"""
struct Vector2D <: AbstractVector{Scalar}
    x::Scalar
    y::Scalar
    Vector2D(x, y) = return Vector2D(Scalar(x), Scalar(y))
    Vector2D(x::Scalar, y::Scalar) = return Vector2D([x,y])
    Vector2D(v::Vector) = return Vector2D(Vector{Scalar}(v))
    Vector2D(v::Vector{Scalar}) = begin
        if length(v) != 2
            error("Vector2D must be 2 dimensional")
        end
        return new(v[1], v[2]) 
    end
end
Base.size(::Vector2D) = return(2,)
Base.getindex(v::Vector2D, i::Int) = begin
    if i == 1
        return v.x
    elseif  i == 2
        return v.y
    else
        error("index $i out of range for Vector2D $v")
    end
end
Base.:(+)(w::Vector2D, v::Vector2D) = Vector2D(w.x+v.x, w.y+v.y)
Base.:(*)(c::Scalar, w::Vector2D) = Vector2D(c * w.x, c * w.y)

"""
    polar_angle(w, transform) -> Angle

Compute the 2D angle of vector `w` from the positive x-axis, in degrees,
after applying `transform` to the raw angle.
"""
polar_angle(w::Vector2D, transform::Function)::Angle = Angle(transform(atand(w.y, w.x)))
polar_angle(w::Vector2D)::Angle = polar_angle(w, identity)

end # module Vector2D