module QuantumGates

using Base: beginsym
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

end # module QuantumGates
