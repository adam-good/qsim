"""
    HelperTypes

Submodule of MathUtils to handle better defined types across the rest of the code.
"""
module HelperTypes

export Scalar

"""
    Scalar

Abstract type for scalar values for the vector space in QSim.
Currently `AbstractFloat` as the space is defined over ℝ²;
Will be updated to `Complex` to represent a Hilbert Space over ℂ².
"""
const Scalar::DataType = AbstractFloat

end # module HelperTypes