using Test

@testset "Quantum State Unittests" begin

    @testset "QState" begin
        using QSim.Quantum.QuantumStates: QState

        @testset "construction" begin
            @test QState(1, 0).vec == [1, 0]
            @test QState(0, 1).vec == [0, 1]
            @test QState([1, 1] / sqrt(2)).vec == [1 / sqrt(2), 1 / sqrt(2)]
        end

        @testset "construction throws" begin
            using QSim.CoreMath.CoreMathErrors: VectorNotNormalException
            @test_throws VectorNotNormalException() QState(1, 1)
        end

        @testset "show" begin
            # TODO: This
        end

        @testset "basis states" begin
            using QSim.Quantum.QuantumStates: KET0, KET1, KETPLUS, KETMINUS
            @test KET0 == QState([1, 0])
            @test KET1 == QState([0, 1])
            @test KETPLUS == QState([1, 1] / sqrt(2))
            @test KETMINUS == QState([1, -1] / sqrt(2))
        end


        @testset "qstate amplitudes" begin
            using QSim.Quantum.QuantumStates: qstate_α, qstate_β, amplitudes
            @test qstate_α(QState(1, 0)) == 1
            @test qstate_β(QState(1, 0)) == 0
            @test amplitudes(QState(1, 0)) == (1, 0)
        end

    end # testset QState
end
