using Test

@testset "Angle Unittests" begin
    using QSim.MathUtils.Angles: Angle

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

        @testset "addition" begin
            @test Angle(3) + Angle(4) == Angle(7)
            @test Angle(270) + Angle(90+45) == Angle(45)
        end

        @testset "subtraction" begin
            @test Angle(10) - Angle(5) == Angle(5)
            @test Angle(90) - Angle(135) == Angle(360-45)
        end
    end

end