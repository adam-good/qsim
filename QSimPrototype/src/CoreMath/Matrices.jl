"""
    MatrixUtils

Submodule of MathUtils to define Unitary Operators on Vector Space V for QSim
"""
module MatrixUtils

using ..ScalarUtils: Scalar
using ..CoreMathErrors: MatrixNotUnitaryException

export UnitaryMatrix, conjugate_transpose

"""
    UnitryMatrix

Unitary Matrix
"""
struct UnitaryMatrix <: AbstractMatrix{Scalar}
    mat::Matrix{Scalar}

    function UnitaryMatrix(matrix::AbstractMatrix)
        if !is_unitary(matrix)
            # TODO: Maybe this should throw a value error?
            throw(MatrixNotUnitaryException("Failed to Construct Unitary Matrix with Given Values"))
        end
        return new(matrix)
    end
end

Base.size(A::UnitaryMatrix) = size(A.mat)
Base.getindex(A::UnitaryMatrix, i::Int) = A.mat[i]
Base.getindex(A::UnitaryMatrix, i::Vararg{Int,2}) = A.mat[i...]

nrows(m::AbstractMatrix)::Int = size(m, 1)
ncols(m::AbstractMatrix)::Int = size(m, 2)
is_square(m::AbstractMatrix)::Bool = nrows(m) == ncols(m)

"""
    identity(n) -> Matrix

Generate the identity matrix of size nxn
"""
identity_matrix(n::Int)::Matrix = begin
    [i == j ? 1 : 0 for i = 1:n, j = 1:n]
end
conjugate_transpose(m::AbstractMatrix)::AbstractMatrix = conj.(transpose(m))
is_unitary(m::AbstractMatrix)::Bool = begin
    if !is_square(m)
        return false
    end
    #TODO: Why isn't isapprox working???
    # isapprox(conjugate_transpose(m)*m, identity_matrix(nrows(m)))
    all([isapprox(a,b) for (a,b) in zip(conjugate_transpose(m)*m, identity_matrix(nrows(m)))])
end

end #module MatrixUtils
