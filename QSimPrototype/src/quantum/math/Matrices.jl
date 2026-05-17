"""
    MatrixUtils

Submodule of MathUtils to define Unitary Operators on Vector Space V for QSim
"""
module MatrixUtils

export UnitaryMatrix, conjugate_transpose

"""
    UnitryMatrix

Unitary Matrix
"""
struct UnitaryMatrix <: AbstractMatrix{Complex}
    mat::Matrix{Complex}

    function UnitaryMatrix(matrix::AbstractMatrix)
        if !is_unitary(matrix)
            error("Unitary Matrix Isn't Unitary")
        end
        return new(matrix)
    end
end

Base.size(A::UnitaryMatrix) = size(A.mat)
Base.getindex(A::UnitaryMatrix, i::Int) = A.mat[i]
Base.getindex(A::UnitaryMatrix, i::Vararg{Int, 2}) = A.mat[i...]

nrows(m::AbstractMatrix)::Int = size(m, 1)
ncols(m::AbstractMatrix)::Int = size(m, 2)
is_2d(m::AbstractMatrix)::Bool = ndims(m) == 2
is_square(m::AbstractMatrix)::Bool = is_2d(m) && nrows(m) == ncols(m)

identity(rows::Int, cols::Int)::Matrix = begin
    [ i == j ? 1 : 0 for i = 1:rows, j = 1:cols ]
end 
conjugate_transpose(m::AbstractMatrix)::AbstractMatrix = conj.(transpose(m))
is_unitary(m::AbstractMatrix)::Bool = begin
    conjugate_transpose(m) * m ≈ identity(nrows(m), ncols(m))
end

end #module MatrixUtils