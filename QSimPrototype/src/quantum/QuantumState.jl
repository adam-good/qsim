module QuantumStates

using ..MathUtils: Vector2D, is_normalized

export QState

"""
    QState

Quantum State represented as a Vector
"""
struct QState
    vec::Vector2D

    QState(vec::Vector2D) = begin
        if !is_normalized(vec)
            error("Vector of Quantum State must be normal")
        end
        return new(vec)
    end
end

qstate_α(state::QState)::Complex = state.vec[1]
qstate_β(state::QState)::Complex = state.vec[2]

amplitudes(ψ::QState) = (ψ.vec[1], ψ.vec[2])

end # module QuantumState