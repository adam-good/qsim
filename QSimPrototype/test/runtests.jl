using Test

@testset "MathUtils" begin
    using QSim.MathUtils

    @testset "Scalar" begin
        @test Scalar === AbstractFloat
    end

    @testset "Angle" begin
        @testset "construction and normalization" begin
            @test Angle(0).value == 0
            @test Angle(360).value == 0
            @test Angle(720).value == 0
            @test Angle(45).value == 45
            @test Angle(-45).value == 315
            @test Angle(450).value == 90
        end

        @testset "show" begin
            @test sprint(show, Angle(45)) == "45°"
        end
    end

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
end
