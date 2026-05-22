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
struct Scalar
    val::AbstractFloat # TODO: Upgrade this to Complex eventually
end

Base.:(≈)(x::Scalar, y::Float64) = isapprox(x.val, y)

Base.:(==)(x::Scalar, y::Scalar) = isapprox(x.val,y.val)
Base.:(+)(x::Scalar, y::Scalar) = scalar(x.val + y.val)
Base.:(-)(x::Scalar, y::Scalar) = scalar(x.val - y.val)
Base.:(*)(x::Scalar, y::Scalar) = scalar(x.val * y.val)
Base.:(/)(x::Scalar, y::Scalar) = scalar(x.val / y.val)
Base.:(^)(x::Scalar, y::Scalar) = scalar(x.val ^ y.val)

Base.:(==)(x::Scalar, y::Number) = isapprox(x.val,y)
Base.:(+)(x::Scalar, y::Number) = scalar(x.val + y)
Base.:(-)(x::Scalar, y::Number) = scalar(x.val - y)
Base.:(*)(x::Scalar, y::Number) = scalar(x.val * y)
Base.:(/)(x::Scalar, y::Number) = scalar(x.val / y)
Base.:(^)(x::Scalar, y::Number) = scalar(x.val ^ y)

Base.:(==)(x::Number, y::Scalar) = isapprox(x.val, y)
Base.:(+)(x::Number, y::Scalar) = scalar(x + y.val)
Base.:(-)(x::Number, y::Scalar) = scalar(x - y.val)
Base.:(*)(x::Number, y::Scalar) = scalar(x * y.val)
Base.:(/)(x::Number, y::Scalar) = scalar(x / y.val)
Base.:(^)(x::Number, y::Scalar) = scalar(x ^ y.val)

scalar(x::Scalar) = x
scalar(x) = Scalar(x)

end