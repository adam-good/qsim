module CoreMath

export Scalar, scalar
export Vector2D, polar_angle, is_normalized
export Angle
export UnitaryMatrix, conjugate_transpose
export VectorNotNormalException

include("Errors.jl")
include("Scalar.jl")
include("Angles.jl")
include("Vectors.jl")
include("Matrices.jl")

using .ScalarUtils: Scalar, scalar
using .VectorUtils: Vector2D, polar_angle, is_normalized
using .Angles: Angle
using .MatrixUtils: UnitaryMatrix, conjugate_transpose



end # module CoreMath
