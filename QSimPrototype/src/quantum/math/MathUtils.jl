module MathUtils

export Vector2D, polar_angle
export Angle

include("Angles.jl")
include("Vectors.jl")

using .VectorUtils: Vector2D, polar_angle
using .Angles: Angle

end # module MathUtils