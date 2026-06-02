module CoreMath

export CoreMathErrors
export ScalarUtils
export VectorUtils
export AngleUtils
export MatrixUtils

include("Errors.jl")
include("Scalar.jl")
include("Angles.jl")
include("Vectors.jl")
include("Matrices.jl")

using .CoreMathErrors
using .ScalarUtils
using .VectorUtils
using .AngleUtils
using .MatrixUtils



end # module CoreMath
