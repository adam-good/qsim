module MathUtils

export Scalar, Angle, Vector2, angle2d, dotprod, born_rule_constraint

const Scalar::DataType = AbstractFloat # NOTE: This will be updated to Complex later

struct Angle
    value::Real

    function Angle(θ::Real)::Angle
        new( (θ + 360) % 360 ) 
    end
end
Base.show(io::IO, x::Angle) = print(io, "$(x.value)°")
Base.convert(::Type{Angle}, x::Real) = Angle(x)

struct Vector2 <: AbstractVector{Scalar}
    x::Scalar
    y::Scalar 
    function Vector2(w::Vector)
        if length(w) != 2
            throw(ErrorException("Vector2 Must be Length 2"))
        end
        return new(w[1],w[2])
    end
end
Base.size(w::Vector2) = return (2,)
Base.getindex(w::Vector2, i::Int) = begin
    if i == 1
        return w.x
    elseif i == 2
        return w.y
    else
        throw(ErrorException("Index Out of Range $i"))
    end
end
Base.getindex(w::Vector2, I::Vararg{Int, 2}) = getindex(w, I) 

born_rule_constraint(w::Vector2)::Bool =  sum(x^2 for x in w) ≈ 1.0

x(w::Vector)::Scalar = w[1]
y(w::Vector)::Scalar = w[2]

angle2d(w::Vector)::Angle = angle2d(convert(Vector{Scalar},w), x -> x)
angle2d(w::Vector, transform::Function)::Angle = angle2d(convert(Vector{Scalar}, w), transform)
angle2d(w::Vector{Scalar}, transform::Function)::Angle = transform(atand(y(w), x(w)))

dotprod(w::Vector, v::Vector)::Scalar = sum(w .* v)
end
