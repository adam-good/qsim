module QuantumStates

using ..MathUtils: Vector2D, is_normalized

export QState, KET0, KET1, KETMINUS, KETPLUS

"""
    QState

Quantum State represented as a 2 Dimensional Vector
"""
struct QState
    vec::Vector2D

    QState(α::Complex, β::Complex) = QState([α, β])
    QState(vec::Vector) = QState(Vector2D(vec))
    QState(vec::Vector2D) = begin
        if !is_normalized(vec)
            error("Vector of Quantum State must be normal")
        end
        return new(vec)
    end
end

Base.show(io::IO, ψ::QState) = print(io, "Quantum State\n  α=$(real(ψ.vec[1]))\n  β=$(real(ψ.vec[2]))")

const KET0 = QState([1,0])
const KET1 = QState([0,1])
const KETPLUS = QState([1,1] / sqrt(2))
const KETMINUS = QState([1,-1] / sqrt(2))

"""
    qstate_α(ψ) -> Scalar

Computes the probability amplitude α associated with |0⟩
"""
qstate_α(state::QState)::Complex = state.vec[1]

"""
   qstate_β

Computes the probability amplitude β associated with |1⟩
"""
qstate_β(state::QState)::Complex = state.vec[2]

"""
    amplitudes(ψ) -> (α, β)

Computes the probability amplitude (α, β) for α|0⟩ + β|1⟩
"""
amplitudes(ψ::QState) = (qstate_α(ψ), qstate_β(ψ))

end # module QuantumState