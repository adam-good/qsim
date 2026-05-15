module MathUtils

export Vector2D, polar_angle, is_normalized
export Angle

include("Angles.jl")
include("Vectors.jl")

using .VectorUtils: Vector2D, polar_angle, is_normalized
using .Angles: Angle

end # module MathUtils