using Test

@testset "Matrix Unittests" begin

    @testset "UnitaryMatrix" begin
        using QSim.CoreMath.MatrixUtils: UnitaryMatrix
        @testset "construction" begin
            @test UnitaryMatrix([0 1; 1 0]).mat == [0 1; 1 0]
            @test UnitaryMatrix([1 1; 1 -1] / sqrt(2)).mat == [1 1; 1 -1] / sqrt(2)
        end

        @testset "construction error" begin
            @test_throws ErrorException("Unitary Matrix Isn't Unitary") UnitaryMatrix([1 2; 3 4])
        end

        @testset "size" begin
            @test size(UnitaryMatrix([0 1; 1 0])) == (2, 2)
            @test size(UnitaryMatrix([1 1; 1 -1] / sqrt(2))) == (2, 2)
            @test size(UnitaryMatrix([0 0 1; 0 1 0; 1 0 0])) == (3, 3)
        end

        @testset "getindex" begin
            @test getindex(UnitaryMatrix([1 1; 1 -1] / sqrt(2)), 4) == -1 / sqrt(2)
            @test UnitaryMatrix([1 1; 1 -1] / sqrt(2))[2, 2] == -1 / sqrt(2)
        end

    end

    @testset "nrows" begin
        using QSim.CoreMath.MatrixUtils: nrows
        @test nrows([1 2;]) == 1
        @test nrows([1 2; 3 4]) == 2
        @test nrows([1 2; 3 4; 5 6]) == 3
    end

    @testset "ncols" begin
        using QSim.CoreMath.MatrixUtils: ncols
        @test ncols([1 2; 3 4; 5 6]) == 2
        @test ncols([1 2 3; 4 5 6]) == 3
    end
    @testset "is_square" begin
        using QSim.CoreMath.MatrixUtils: is_square
        @test is_square([1 2; 3 4]) == true
        @test is_square([1 2 3; 4 5 6]) == false
    end

    @testset "identity_matrix" begin
        using QSim.CoreMath.MatrixUtils: identity_matrix
        @test identity_matrix(2) == [1 0; 0 1]
        @test identity_matrix(3) == [1 0 0; 0 1 0; 0 0 1]
        @test identity_matrix(4) == [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1]
    end

    @testset "conjugate_transpose" begin
        using QSim.CoreMath.MatrixUtils: conjugate_transpose
        @test conjugate_transpose([1 -2-im 5; 1+im im 4-2im]) == [1 1-im; -2+im -im; 5 4+2im]
        @test conjugate_transpose([1 2 3; 4 5 6]) == [1 4; 2 5; 3 6]
    end

    @testset "is_unitary" begin
        using QSim.CoreMath.MatrixUtils: is_unitary
        @test is_unitary([0 1; 1 0]) == true
        @test is_unitary([1 1; 1 -1] / sqrt(2)) == true
        @test is_unitary([1 1; 1 1]) == false
        @test is_unitary([0 0 1; 1 0 0]) == false
    end

end
