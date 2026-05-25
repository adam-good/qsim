using Test

@testset "Unit Tests" begin
    include("test_CoreMath/test_CoreMath.jl")
    include("test_Quantum/test_Quantum.jl")
end
