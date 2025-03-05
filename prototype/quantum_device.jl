module QuDevice
include("qubit.jl")

using ..Qubits:
    Qubit

mutable struct QuantumDevice
    N::Int
    allocated::Int
    QuantumDevice(n::Int) = begin
        new(n,0)
    end
end

function qalloc!(device::QuantumDevice)
    if device.allocated >= device.N
        throw("NO")
    end
    q = Qubit(0.0)
    device.allocated = device.allocated + 1
    return q
end

function qfree!(device::QuantumDevice, q::Qubit)
    q = nothing
    device.allocated = device.allocated - 1
end

end