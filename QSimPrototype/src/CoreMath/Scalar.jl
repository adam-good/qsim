"""
    ScalarUtils

Submodule of CoreMath to define the set of scalars 𝕊 for vector space V
"""
module ScalarUtils

using Base: isgreater
export Scalar, scalar

"""
    Scalar

Currently ℝ but will soon be Upgraded to ℂ
"""
struct Scalar <: Real
    val::Float64 # TODO: Upgrade this to Complex eventually
end

# Addition
Base.:(+)(x::Scalar, y::Scalar) = Scalar(x.val + y.val)
Base.:(+)(x::Scalar, y::Real)   = Scalar(x.val + y)
Base.:(+)(x::Real, y::Scalar)   = Scalar(x     + y.val)

# Subtraction
Base.:(-)(x::Scalar, y::Scalar) = Scalar(x.val - y.val)
Base.:(-)(x::Scalar, y::Real)   = Scalar(x.val - y)
Base.:(-)(x::Real, y::Scalar)   = Scalar(x     - y.val)

# Multiplication
Base.:(*)(x::Scalar, y::Scalar) = Scalar(x.val * y.val)
Base.:(*)(x::Scalar, y::Real)   = Scalar(x.val * y)
Base.:(*)(x::Real, y::Scalar)   = Scalar(x     * y.val)

# Division
Base.:(/)(x::Scalar, y::Scalar) = Scalar(x.val / y.val)
Base.:(/)(x::Scalar, y::Real)   = Scalar(x.val / y)
Base.:(/)(x::Real, y::Scalar)   = Scalar(x     / y.val)

# # Power
# Base.:(^)(x::Scalar, y::Scalar) = Scalar(x.val ^ y.val)
# Base.:(^)(x::Scalar, y::Real)   = Scalar(x.val ^ y)
# Base.:(^)(x::Real, y::Scalar)   = Scalar(x     ^ y.val)

# Comparisons
Base.isapprox(x::Scalar, y::Scalar) = isapprox(x.val, y.val)
Base.isapprox(x::Scalar, y::Real)   = isapprox(x.val, y)
Base.isapprox(x::Real, y::Scalar)   = isapprox(x    , y.val)

Base.:(==)(x::Scalar, y::Scalar) = isapprox(x.val, y.val)
Base.:(==)(x::Scalar, y::Real)   = isapprox(x.val, y)
Base.:(==)(x::Real, y::Scalar)   = isapprox(x    , y.val)

Base.isless(x::Scalar, y::Scalar) = isless(x.val, y.val)
Base.isless(x::Scalar, y::Real)   = isless(x.val, y)
Base.isless(x::Real, y::Scalar)   = isless(x    , y.val)

Base.isgreater(x::Scalar, y::Scalar) = isgreater(x.val, y.val)
Base.isgreater(x::Scalar, y::Real)   = isgreater(x.val, y)
Base.isgreater(x::Real, y::Scalar)   = isgreater(x    , y.val)

# Identities
Base.one(::Scalar)  = Scalar(1)
Base.zero(::Scalar) = Scalar(0)

# Transformations
Base.transpose(x::Scalar) = x
Base.conj(x::Scalar) = x # TODO: This must change when Scalar is upgraded to complex

# Conversions
Base.convert(::Type{Scalar}, x::Int64) = Scalar(x)
Base.convert(::Type{Scalar}, x::Float64) = Scalar(x)

# Display Functions
Base.show(io::IO, x::Scalar) = print(io, "$(x.val)")
Base.show(io::IO, w::AbstractVector{Scalar}) = begin
    for x in w
        print(io, "$x ")
    end
    print(io, "\n")
end

scalar(x::Scalar) = x
scalar(x) = Scalar(x)

end
