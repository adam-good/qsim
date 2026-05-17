using Test

include("test_Angles.jl")
include("test_Matrices.jl")

@testset "MathUtils" begin
    using QSim.MathUtils

    @testset "polar_angle" begin
        @testset "with identity transform" begin
            @test polar_angle([1.0, 0.0]).value == 0
            @test polar_angle([0.0, 1.0]).value == 90
            @test polar_angle([-1.0, 0.0]).value == 180
            @test polar_angle([0.0, -1.0]).value == 270
        end

        @testset "with custom transform" begin
            @test polar_angle([1.0, 0.0], x -> 2 * x).value == 0
            @test polar_angle([0.0, 1.0], x -> 2 * x).value == 180
            @test polar_angle([1.0, 1.0], x -> 2 * x).value == 90
        end
    end

    @testset "is_normalized" begin
        @test is_normalized([1.0, 0.0]) == true
        @test is_normalized([0.0, 1.0]) == true
        @test is_normalized([1/sqrt(2), 1/sqrt(2)]) == true
        @test is_normalized([1.0, 1.0]) == false
    end

end

@testset "Quantum" begin
    using QSim.Quantum

    @testset "QState" begin
        
        @testset "construction" begin
            @test QState([1,0]).vec == [1,0]
        end

        @testset "show" begin
            @test sprint(show, QState([1,0])) == "Quantum State\n  α=1\n  β=0"
            @test sprint(show, QState([0,1])) == "Quantum State\n  α=0\n  β=1"
            @test sprint(show, QState([1,1] / sqrt(2))) == "Quantum State\n  α=$(1/sqrt(2))\n  β=$(1/sqrt(2))"
            @test sprint(show, QState([1,-1] / sqrt(2))) == "Quantum State\n  α=$(1/sqrt(2))\n  β=$(-1/sqrt(2))"
        end
        
    end
end