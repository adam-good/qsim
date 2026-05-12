module Quantum

export Basis 

"""
    Basis

Represents an orthonormal basis for a quantum Hilbert space.
Each element is a state vector in `Vector{Scalar}` form.
"""
struct Basis
    vectors::Vector{State}

    function Basis(a::State, b::State)
        return Basis([a, b])
    end

    function Basis(vecs::Vector{State})
        # TODO: Check vectors are all orthogonal
        return new(vecs)
    end
end

Base.getindex(basis::Basis, idx) = basis.vectors[idx]

"""
    ZBasis

The computational (Z) basis: `|0⟩ = [1, 0]` and `|1⟩ = [0, 1]`.
"""
const ZBasis = Basis(KET0, KET1)

"""
    XBasis

The computational (X) basis: `|+⟩ = [1/√2, 1/√2]` and `|-⟩ = [1/√2,-1/√2]`
"""
const XBasis = Basis(KETPLUS, KETMINUS)

end