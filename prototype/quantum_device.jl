module QuDevice
include("qubit.jl")

using ..Qubits:
    Qubit

mutable struct QuantumDevice
    N::Int
    Q::Vector{Qubit}
    function qalloc()
        q = Q[N]
        N = N-1
        return q
    end
    # function qfree(q::Qubit)
    #     N = N+1
    # end

    QuantumDevice(n::Int) = begin
        new(n, [Qubit(0.0) for i=1:n])
    end
end

function qalloc!(device::QuantumDevice)
    q = device.Q[device.N]
    device.N = device.N - 1
    return q
end

end