"""
    CoreMathErrors

Submodule of CoreMath that contains all of the relevant exception types
"""
module CoreMathErrors

export VectorNotNormalException
export MatrixNotUnitaryException
export DimensionSizeMismatchError

struct DimensionSizeMismatchError <: Exception
    msg::String
    rank::Int
    expected::Int
    found::Int
end
Base.showerror(io::IO, err::DimensionSizeMismatchError) = begin
    print(io, "DimensionSizeMismatch: ")
    print(io, err.msg)
    print(io, "    rank:     $(err.rank)")
    print(io, "    expected: $(err.expected)")
    print(io, "    found:    $(err.found)")
end

struct VectorNotNormalException <: Exception
    msg::String
end

struct MatrixNotUnitaryException <: Exception
    msg::String
end

end
