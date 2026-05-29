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
    value::Float64 # TODO: Upgrade this to Complex eventually
end

# Addition
Base.:(+)(x::Scalar, y::Scalar) = Scalar(x.value + y.value)
Base.:(+)(x::Scalar, y::Real)   = Scalar(x.value + y)
Base.:(+)(x::Real,   y::Scalar) = Scalar(x       + y.value)

# Subtraction
Base.:(-)(x::Scalar, y::Scalar) = Scalar(x.value - y.value)
Base.:(-)(x::Scalar, y::Real)   = Scalar(x.value - y)
Base.:(-)(x::Real,   y::Scalar) = Scalar(x       - y.value)

# Multiplication
Base.:(*)(x::Scalar, y::Scalar) = Scalar(x.value * y.value)
Base.:(*)(x::Scalar, y::Real)   = Scalar(x.value * y)
Base.:(*)(x::Real,   y::Scalar) = Scalar(x       * y.value)

# Division
Base.:(/)(x::Scalar, y::Scalar) = Scalar(x.value / y.value)
Base.:(/)(x::Scalar, y::Real)   = Scalar(x.value / y)
Base.:(/)(x::Real,   y::Scalar) = Scalar(x       / y.value)

# # Power
# Base.:(^)(x::Scalar, y::Scalar) = Scalar(x.val ^ y.val)
# Base.:(^)(x::Scalar, y::Real)   = Scalar(x.val ^ y)
# Base.:(^)(x::Real, y::Scalar)   = Scalar(x     ^ y.val)

# Comparisons
Base.isapprox(x::Scalar, y::Scalar) = isapprox(x.value, y.value)
Base.isapprox(x::Scalar, y::Real)   = isapprox(x.value, y)
Base.isapprox(x::Real,   y::Scalar) = isapprox(x      , y.value)

Base.:(==)(x::Scalar, y::Scalar) = isapprox(x.value, y.value)
Base.:(==)(x::Scalar, y::Real)   = isapprox(x.value, y)
Base.:(==)(x::Real,   y::Scalar) = isapprox(x      , y.value)

Base.isless(x::Scalar, y::Scalar) = isless(x.value, y.value)
Base.isless(x::Scalar, y::Real)   = isless(x.value, y)
Base.isless(x::Real,   y::Scalar) = isless(x      , y.value)

Base.isgreater(x::Scalar, y::Scalar) = isgreater(x.value, y.value)
Base.isgreater(x::Scalar, y::Real)   = isgreater(x.value, y)
Base.isgreater(x::Real,   y::Scalar) = isgreater(x      , y.value)

# Identities
Base.one(::Scalar)  = Scalar(1)
Base.zero(::Scalar) = Scalar(0)

# Transformations
Base.transpose(x::Scalar) = x
Base.conj(x::Scalar) = x # TODO: This must change when Scalar is upgraded to complex

# Display Functions
Base.show(io::IO, x::Scalar) = print(io, "$(x.value)")
Base.show(io::IO, w::AbstractVector{Scalar}) = begin
    for x in w
        print(io, "$x ")
    end
    print(io, "\n")
end

scalar(x::Scalar) = x
scalar(x) = Scalar(x)

end
