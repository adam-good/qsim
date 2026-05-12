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

        @testset "convert" begin
            @test convert(Angle, 90) == Angle(90)
            @test convert(Angle, -270) == Angle(90)
        end
    end

    @testset "born_rule_constraint" begin
        @test born_rule_constraint([1.0, 0.0]) == true
        @test born_rule_constraint([0.0, 1.0]) == true
        @test born_rule_constraint([1 / sqrt(2), 1 / sqrt(2)]) == true
        @test born_rule_constraint([0.6, 0.8]) == true
        @test born_rule_constraint([1.0, 1.0]) == false
        @test born_rule_constraint([0.5, 0.5]) == false
        @test born_rule_constraint([1.0, 0.0, 0.0]) == true
    end

    @testset "vec_x" begin
        @test vec_x([3.0, 4.0]) == 3.0
        @test vec_x([1.0, 0.0]) == 1.0
    end

    @testset "vec_y" begin
        @test vec_y([3.0, 4.0]) == 4.0
        @test vec_y([1.0, 0.0]) == 0.0
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

    @testset "dotprod" begin
        @test dotprod([1.0, 0.0], [1.0, 0.0]) == 1.0
        @test dotprod([1.0, 0.0], [0.0, 1.0]) == 0.0
        @test dotprod([1.0, 1.0], [1.0, 0.0]) == 1.0
        @test dotprod([1 / sqrt(2), 1 / sqrt(2)], [1 / sqrt(2), 1 / sqrt(2)]) ≈ 1.0
    end
end

@testset "Quantum" begin
    using QSim.MathUtils
    using QSim.MathUtils: Scalar, Angle
    using QSim.Quantum: Quantum,
        State,
        Basis,
        vector,
        state_angle,
        bloch_angle,
        amplitude,
        probability,
        ZBasis,
        XBasis,
        KET0,
        KET1,
        KETPLUS,
        KETMINUS

    function vec_approx(a::Vector, b::Vector)
        @test length(a) == length(b)
        for (x, y) in zip(a, b)
            @test x ≈ y
        end
    end

    @testset "Basis" begin
        @testset "construction from two Vectors" begin
            b = Basis([1.0, 0.0], [0.0, 1.0])
            vec_approx(b[1], [1.0, 0.0])
            vec_approx(b[2], [0.0, 1.0])
        end

        @testset "ZBasis" begin
            vec_approx(ZBasis[1], [1.0, 0.0])
            vec_approx(ZBasis[2], [0.0, 1.0])
        end

        @testset "XBasis" begin
            vec_approx(XBasis[1], [1 / sqrt(2), 1 / sqrt(2)])
            vec_approx(XBasis[2], [1 / sqrt(2), -1 / sqrt(2)])
        end
    end

    @testset "State" begin
        @testset "from Vector" begin
            @testset "valid length 2" begin
                ψ = State([1.0, 0.0])
                @test ψ.α == 1.0
                @test ψ.β == 0.0
            end

            @testset "invalid length throws" begin
                @test_throws ErrorException State([1.0])
                @test_throws ErrorException State([1.0, 0.0, 0.0])
                @test_throws ErrorException State([1.0, 0.0, 0.0, 0.0])
            end
        end

        @testset "from scalars" begin
            @testset "born rule satisfied" begin
                ψ = State(1, 0)
                @test ψ.α == 1.0
                @test ψ.β == 0.0

                ψ = State(0, 1)
                @test ψ.α == 0.0
                @test ψ.β == 1.0

                ψ = State(1 / sqrt(2), 1 / sqrt(2))
                @test ψ.α == 1 / sqrt(2)
                @test ψ.β == 1 / sqrt(2)

                ψ = State(0.6, 0.8)
                @test ψ.α == 0.6
                @test ψ.β == 0.8
            end

            @testset "born rule violated throws DomainError" begin
                @test_throws DomainError State(1.0, 1.0)
                @test_throws DomainError State(0.5, 0.5)
            end
        end

        @testset "show" begin
            @test sprint(show, KET0) == "|0.0°⟩"
            @test sprint(show, KET1) == "|90.0°⟩"
        end
    end

    @testset "KET constants" begin
        @testset "KET0" begin
            @test KET0.α == 1.0
            @test KET0.β == 0.0
        end

        @testset "KET1" begin
            @test KET1.α == 0.0
            @test KET1.β == 1.0
        end

        @testset "KETPLUS" begin
            @test KETPLUS.α == 1 / sqrt(2)
            @test KETPLUS.β == 1 / sqrt(2)
        end

        @testset "KETMINUS" begin
            @test KETMINUS.α == 1 / sqrt(2)
            @test KETMINUS.β == -1 / sqrt(2)
        end
    end

    @testset "vector" begin
        @testset "in ZBasis" begin
            vec_approx(vector(KET0), [1.0, 0.0])
            vec_approx(vector(KET1), [0.0, 1.0])
            vec_approx(vector(KETPLUS), [1 / sqrt(2), 1 / sqrt(2)])
            vec_approx(vector(KETMINUS), [1 / sqrt(2), -1 / sqrt(2)])
        end

        @testset "in XBasis" begin
            vec_approx(vector(KET0, XBasis), [1 / sqrt(2), 1 / sqrt(2)])
            vec_approx(vector(KET1, XBasis), [1 / sqrt(2), -1 / sqrt(2)])
            vec_approx(vector(KETPLUS, XBasis), [1.0, 0.0])
            vec_approx(vector(KETMINUS, XBasis), [0.0, 1.0])
        end
    end

    @testset "state_angle" begin
        @test state_angle(KET0).value == 0
        @test state_angle(KET1).value == 90
        @test state_angle(KETPLUS).value == 45
        @test state_angle(KETMINUS).value == 315
    end

    @testset "bloch_angle" begin
        @test bloch_angle(KET0).value == 0
        @test bloch_angle(KET1).value == 180
        @test bloch_angle(KETPLUS).value == 90
        @test bloch_angle(KETMINUS).value == 270
    end

    @testset "amplitude" begin
        @test amplitude(KET0, KET0) ≈ 1.0
        @test amplitude(KET0, KET1) ≈ 0.0
        @test amplitude(KET1, KET0) ≈ 0.0
        @test amplitude(KET1, KET1) ≈ 1.0
        @test amplitude(KET0, KETPLUS) ≈ 1 / sqrt(2)
        @test amplitude(KETPLUS, KETPLUS) ≈ 1.0
        @test amplitude(KETPLUS, KETMINUS) ≈ 0.0
    end

    @testset "probability" begin
        @test probability(KET0, KET0) ≈ 1.0
        @test probability(KET0, KET1) ≈ 0.0
        @test probability(KET1, KET0) ≈ 0.0
        @test probability(KET1, KET1) ≈ 1.0
        @test probability(KET0, KETPLUS) ≈ 0.5
        @test probability(KETPLUS, KETPLUS) ≈ 1.0
        @test probability(KETPLUS, KETMINUS) ≈ 0.0
    end
end
