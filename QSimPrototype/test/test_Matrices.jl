using Test

@testset "MathUtils" begin
    using QSim.MathUtils.MatrixUtils: UnitaryMatrix

    @testset "UnitaryMatrix" begin
       
        @testset "construction" begin
            @test UnitaryMatrix([0 1; 1 0]).mat == [0 1; 1 0]
            @test UnitaryMatrix([1 1; 1 -1] / sqrt(2)).mat == [1 1; 1 -1] / sqrt(2)
        end

        @testset "construction error" begin
            @test_throws ErrorException("Unitary Matrix Isn't Unitary") UnitaryMatrix([1 2; 3 4])
        end

    end

    @testset "identity" begin
        using QSim.MathUtils.MatrixUtils: identity
        @test identity(2, 2) == [1 0; 0 1;]
        @test identity(3, 3) == [1 0 0; 0 1 0; 0 0 1;]
        @test identity(4, 4) == [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1;]
    end

    @testset "conjugate_transpose" begin
        using QSim.MathUtils.MatrixUtils: conjugate_transpose
        @test conjugate_transpose([1 -2-im 5; 1+im im 4-2im]) == [1 1-im; -2+im -im; 5 4+2im ]
        @test conjugate_transpose([1 2 3; 4 5 6]) == [1 4; 2 5; 3 6]
    end

    @testset "is_unitary" begin
        using QSim.MathUtils.MatrixUtils: is_unitary
        @test is_unitary([0 1; 1 0]) == true
        @test is_unitary([1 1; 1 -1] / sqrt(2)) == true
        @test is_unitary([1 1; 1 1]) == false
    end
end