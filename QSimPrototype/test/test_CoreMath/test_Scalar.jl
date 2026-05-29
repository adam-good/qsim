using Test

@testset "Scalar Unit Tests" begin
    using  QSim.CoreMath.ScalarUtils: Scalar

    @testset "Scalar" begin
        @testset "construction" begin
            @test Scalar(Int64(5)).value == 5.0
            @test Scalar(Float64(3.14)).value == 3.14
        end

        @testset "show" begin
            @test sprint(show, Scalar(3.14)) == "3.14"
        end

        @testset "addition" begin
            x = 1.2; y = 2.1
            target = Scalar(3.3)
            z1 = Scalar(x) + Scalar(y)
            z2 = Scalar(x) + y
            z3 = x         + Scalar(y)
            @test z1 isa Scalar
            @test z1 == target
            @test z2 isa Scalar
            @test z2 == target
            @test z3 isa Scalar
            @test z3 == target
        end

        @testset "subtraction" begin
            x = 3.3; y = 2.1
            target = Scalar(1.2)
            z1 = Scalar(x) - Scalar(y)
            z2 = Scalar(x) - y
            z3 = x         - Scalar(y)
            @test z1 isa Scalar
            @test z1 == target
            @test z2 isa Scalar
            @test z2 == target
            @test z3 isa Scalar
            @test z3 == target
        end

        @testset "multiplication" begin
            x = 2; y = 3
            target = Scalar(6)
            z1 = Scalar(x) * Scalar(y)
            z2 = Scalar(x) * y
            z3 = x         * Scalar(y)
            @test z1 isa Scalar
            @test z1 == target
            @test z2 isa Scalar
            @test z2 == target
            @test z3 isa Scalar
            @test z3 == target
        end


        @testset "division" begin
            x = 6; y = 3
            target = Scalar(2)
            z1 = Scalar(x) / Scalar(y)
            z2 = Scalar(x) / y
            z3 = x         / Scalar(y)
            @test z1 isa Scalar
            @test z1 == target
            @test z2 isa Scalar
            @test z2 == target
            @test z3 isa Scalar
            @test z3 == target
        end

        @testset "power" begin
            x = 2; y = 4
            target = Scalar(16)
            z = Scalar(x) ^ Scalar(y)
            @test z == target
        end

        @testset "isapprox" begin
            @test isapprox(Scalar(5), Scalar(5.0-eps(5.)))   == true
            @test isapprox(Scalar(5), 5.0-eps(5.))           == true
            @test isapprox(5        , Scalar(5.0-eps(5.)))   == true
            @test isapprox(Scalar(5), Scalar(6.0)) == false
        end

        @testset "equivalence" begin
            @test (Scalar(5.0) == Scalar(5.0)) == true
            @test (Scalar(5.0) == 5.0        ) == true
            @test (5.0         == Scalar(5.0)) == true
            @test (Scalar(5.0) == Scalar(6.0)) == false
        end

        @testset "isless" begin
            @test isless(Scalar(5.0) , Scalar(6.0)) == true
            @test isless(Scalar(5.0) , 6.0)
            @test isless(5.0         , Scalar(6.0))
            @test isless(Scalar(6.0), Scalar(5.0)) == false
        end

        @testset "identities" begin
            @test one(Scalar) == Scalar(1)
            @test zero(Scalar) == Scalar(0)
        end

        @testset "transformations" begin
            @test transpose(Scalar(5)) == Scalar(5)
            @test conj(Scalar(5)) == Scalar(5)
        end
    end
end
