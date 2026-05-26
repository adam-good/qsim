"""
    ScalarUtils

Submodule of CoreMath to define the set of scalars 𝕊 for vector space V
"""
module ScalarUtils

export Scalar, scalar

"""
    Scalar

Currently ℝ but will soon be Upgraded to ℂ
"""
struct Scalar <: Real
    val::Float64 # TODO: Upgrade this to Complex eventually
end

# TODO: Needs updated when Scalar is upgraded to complex
Base.Float64(x::Scalar)::Float64 = x.val
Base.float(x::Scalar)::AbstractFloat = x.val

Base.isapprox(x::Scalar, y::Scalar) = isapprox(x.val, y.val)
Base.isapprox(x::Scalar, y::AbstractFloat) = isapprox(x.val, y)
Base.isapprox(x::Scalar, y::Int) = isapprox(x.val, y)

Base.:(==)(x::Scalar, y::Scalar) = isapprox(x.val, y.val)
Base.:(+)(x::Scalar, y::Scalar) = scalar(x.val + y.val)
Base.:(-)(x::Scalar, y::Scalar) = scalar(x.val - y.val)
Base.:(*)(x::Scalar, y::Scalar) = scalar(x.val * y.val)
Base.:(/)(x::Scalar, y::Scalar) = scalar(x.val / y.val)
Base.:(^)(x::Scalar, y::Scalar) = scalar(x.val ^ y.val)

Base.:(==)(x::Scalar, y::Real) = isapprox(x.val, y)
Base.:(+)(x::Scalar, y::Real) = scalar(x.val + y)
Base.:(-)(x::Scalar, y::Real) = scalar(x.val - y)
Base.:(*)(x::Scalar, y::Real) = scalar(x.val * y)
Base.:(/)(x::Scalar, y::Real) = scalar(x.val / y)
# Base.:(^)(x::Scalar, y::Real) = scalar(x.val^y)

Base.:(==)(x::Real, y::Scalar) = isapprox(x.val, y)
Base.:(+)(x::Real, y::Scalar) = scalar(x + y.val)
Base.:(-)(x::Real, y::Scalar) = scalar(x - y.val)
Base.:(*)(x::Real, y::Scalar) = scalar(x * y.val)
Base.:(/)(x::Real, y::Scalar) = scalar(x / y.val)
# Base.:(^)(x::Real, y::Scalar) = scalar(x^y.val)

Base.zero(::Scalar) = Scalar(0)
Base.transpose(x::Scalar) = x
Base.conj(x::Scalar) = x # TODO: This must change when Scalar is upgraded to complex

Base.convert(::Type{Scalar}, x::Int64) = Scalar(x)
Base.convert(::Type{Scalar}, x::Float64) = Scalar(x)

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
