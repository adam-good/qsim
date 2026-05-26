module QuantumGates

using ..QuantumStates: QState
using ..Matrices: UnitaryMatrix

struct QGate
    mat::UnitaryMatrix
    QGate(mat::Matrix) = new(UnitaryMatrix(mat))
end

Base.show(io::IO, U::QGate) = begin
    print(io, "Quantum Gate\n")
    for row in eachrow(U.mat)
        print(io, "    $row")
    end
end

Base.:(*)(U::QGate, V::QGate)::QGate = QGate(U.mat * V.mat)
Base.:(*)(U::QGate, ψ::QState)::QState = QState(U.mat * ψ.vec)

end # module QuantumGates
