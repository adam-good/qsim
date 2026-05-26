using Test

@testset "Quantum Gate Unittests" begin

    @testset "QGate" begin
        using QSim.Quantum.QuantumGates: QGate

        @testset "construction" begin
            @test QGate([0 1; 1 0]).mat == [0 1; 1 0]
            @test QGate([1 1; 1 -1] / sqrt(2)).mat == [1 1; 1 -1] / sqrt(2)
        end

        @testset "show" begin
            # TODO: This
        end

        @testset "multiplication" begin
            # @test QGate([0 1; 1 0]) * QGate([1 1; 1 -1] / sqrt(2)) == QGate([1 -1; 1 1] / sqrt(2))
        end
    end
end
