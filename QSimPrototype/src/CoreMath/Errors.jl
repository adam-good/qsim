"""
    CoreMathErrors

Submodule of CoreMath that contains all of the relevant exception types
"""
module CoreMathErrors

export VectorNotNormalException
export MatrixNotUnitaryException

struct VectorNotNormalException <: Exception
    msg::String
    VectorNotNormalException() = new("Expected Normalized Vector")
end

struct MatrixNotUnitaryException <: Exception
    msg::String
    MatrixNotUnitaryException() = new("Expected Unitary Matrix.")
end

end
