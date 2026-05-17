module Angles

export Angle

"""
    Angle(value::Real)

Represents a planar angle in degrees, normalized to [0,360)
"""
struct Angle
    value::Real

    function Angle(θ::Real)
        return new((θ + 360) % 360)
    end
end
Base.show(io::IO, θ::Angle) = print(io, "$(θ.value)°")
Base.:(+)(θ::Angle, ϕ::Angle) = Angle(θ.value + ϕ.value)
Base.:(-)(θ::Angle, ϕ::Angle) = Angle(θ.value - ϕ.value)
 
end