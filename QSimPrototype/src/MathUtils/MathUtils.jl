module MathUtils

export Scalar, Vector2D, Angle

include("HelperTypes.jl")
include("Vector2D.jl")
include("Angle.jl")

using .HelperTypes: Scalar
using .VectorUtils: Vector2D
using .Angles: Angle

end # module MathUtils