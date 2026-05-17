module MathUtils

export Vector2D, polar_angle, is_normalized
export Angle
export UnitaryMatrix, conjugate_transpose 

include("Angles.jl")
include("Vectors.jl")
include("Matrices.jl")

using .VectorUtils: Vector2D, polar_angle, is_normalized
using .Angles: Angle
using .MatrixUtils: UnitaryMatrix, conjugate_transpose

end # module MathUtils