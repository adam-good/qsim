using Test

include("test_Angles.jl")
include("test_Matrices.jl")
include("test_Vectors.jl")


# CoreMath Integration Tests 
@testset "CoreMath" begin
    using QSim.CoreMath

    @testset "polar_angle" begin

        @testset "identity transform" begin
            @test polar_angle([1.0, 0.0]).value == 0
            @test polar_angle([0.0, 1.0]).value == 90
            @test polar_angle([-1.0, 0.0]).value == 180
            @test polar_angle([0.0, -1.0]).value == 270           
        end # testset identity transform

        @testset "with custom transform" begin
            @test polar_angle([1.0, 0.0], x -> 2 * x).value == 0
            @test polar_angle([0.0, 1.0], x -> 2 * x).value == 180
            @test polar_angle([1.0, 1.0], x -> 2 * x).value == 90
        end # testset custom transform

    end # testset polar_angle

    
end # testset CoreMath