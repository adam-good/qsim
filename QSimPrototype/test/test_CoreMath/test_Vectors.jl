using Test

@testset "Vector Unittests" begin
    
    @testset "Vector2D" begin
        using QSim.CoreMath.VectorUtils: Vector2D
        @testset "construction" begin
            w = Vector2D(1, 0)
            @test w.x == 1
            @test w.y == 0
            v = Vector2D([1,-1] / 2)
            @test v.x == 0.5
            @test v.y == -0.5
        end

        @testset "construction error" begin
            @test_throws ErrorException("Vector2D must be 2 dimensional") Vector2D([1])
            @test_throws ErrorException("Vector2D must be 2 dimensional") Vector2D([1,2,3])
        end

        @testset "size" begin
            @test size(Vector2D(1,0)) == (2,)
        end

        @testset "getindex" begin
            v = Vector2D(1,0)
            @test v[1] == 1
            @test v[2] == 0
        end

        @testset "addition" begin
            v = Vector2D(1,0)
            w = Vector2D(1,1)
            @test v+w == Vector2D(2,1)
        end

        @testset "multiplication" begin
            w = Vector2D(1,1)
            @test 2 * w == Vector2D(2,2) 
        end
    end

    @testset "vec x and y" begin
        using QSim.CoreMath.VectorUtils: vec_x, vec_y
        w = Vector2D(1,0)
        @test vec_x(w) == 1
        @test vec_y(w) == 0
    end

    @testset "norm2" begin
        using QSim.CoreMath.VectorUtils: norm2
        @test norm2([1,2]) ≈ 5.0
        @test norm2([1,1] / sqrt(2)) ≈ 1.0
    end

    @testset "is_normalized" begin
        using QSim.CoreMath.VectorUtils: is_normalized
        @test is_normalized([1,0]) == true
        @test is_normalized([0,1]) == true
        @test is_normalized([1,1] / sqrt(2)) == true
        @test is_normalized([1,1]) == false        
    end

end # testset Vector Unittests