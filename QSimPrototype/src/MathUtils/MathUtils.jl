module MathUtils

export Scalar
export Vector2D, polar_angle
export Angle

include("HelperTypes.jl")
include("Angle.jl")
include("Vector2D.jl")

using .HelperTypes: Scalar
using .VectorUtils: Vector2D, polar_angle
using .Angles: Angle

end # module MathUtils