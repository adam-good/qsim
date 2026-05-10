module MathUtils

export Scalar, Angle, angle2d, dotprod, born_rule_constraint

const Scalar::DataType = AbstractFloat # NOTE: This will be updated to Complex later

struct Angle
    value::Real

    function Angle(θ::Real)::Angle
        new( (θ + 360) % 360 ) 
    end
end
Base.show(io::IO, x::Angle) = print(io, "$(x.value)°")
Base.convert(::Type{Angle}, x::Real) = Angle(x)

born_rule_constraint(w::Vector{Scalar})::Bool =  sum(x^2 for x in w) ≈ 1.0

x(w::Vector{Scalar})::Scalar = w[1]
y(w::Vector{Scalar})::Scalar = w[2]

angle2d(w::Vector)::Angle                              = angle2d(convert(Vector{Scalar},w), x -> x)
angle2d(w::Vector, transform::Function)::Angle         = angle2d(convert(Vector{Scalar}, w), transform)
angle2d(w::Vector{Scalar}, transform::Function)::Angle = transform(atand(y(w), x(w)))

dotprod(w::Vector, v::Vector)::Scalar = sum(w .* v)
end