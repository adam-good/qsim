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
    rank::Int64
    expected::Int64
    found::Int64
end
DimensionSizeMismatchError(; msg::String, rank::Int, expected::Int, found::Int) = DimensionSizeMismatchError(msg,rank,expected,found) # Keyword arg support
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

# TODO: Is there a field I can add here to show the issue?
struct MatrixNotUnitaryException <: Exception
    msg::String
end
Base.showerror(io::IO, err::MatrixNotUnitaryException) = begin
	print(io, "MatrixNotUnitaryException: ")
	print(io, err.msg)
end

end
