# AGENTS.md - QSimPrototype

## Project Overview

**QSim** is a Julia quantum simulation library. The main package is in `QSimPrototype/`.

---

## Build / Test Commands

### Package Operations

```bash
# Load the package (builds if needed)
julia --project=QSimPrototype -e 'using QSim'

# Build the package
julia --project=QSimPrototype -e 'using Pkg; Pkg.build()'

# Update dependencies
julia --project=QSimPrototype -e 'using Pkg; Pkg.update()'
```

### Running Tests

```bash
# Run all tests (direct include approach)
julia --project=QSimPrototype -e 'using Test; include("test/runtests.jl")'

# Run tests with package precompiled first
julia --project=QSimPrototype -e 'using Pkg; Pkg.precompile(); using Test; include("test/runtests.jl")'

# Run a specific @testset
julia --project=QSimPrototype -e '
    using Test
    using QSim
    @testset "My Test" begin
        @test 1 == 1
    end
'
```

### Linting / Formatting

```bash
# Format code (requires JuliaFormatter.jl)
julia --project=QSimPrototype -e 'using JuliaFormatter; format(".")'

# Lint with CodeQuality.jl tools
julia --project=QSimPrototype -e 'using Aqua, JuliaFormatter; Aqua.test_all(QSim)'
```

### Interactive REPL

```bash
# Start REPL with package loaded
julia --project=QSimPrototype
# Then: using QSim
```

---

## Code Style Guidelines

References: [Julia Style Guide](https://docs.julialang.org/en/v1/manual/style-guide/),
[Blue Style Guide](https://github.com/invenia/BlueStyle),
[Julia Formatting Guidelines](https://docs.julialang.org/en/v1.13-dev/devdocs/contributing/formatting/).

### Naming Conventions

| Element          | Convention       | Example                               |
|------------------|------------------|---------------------------------------|
| Modules/Packages | PascalCase       | `MathUtils`, `Quantum`                 |
| Types/Structs    | PascalCase       | `Angle`, `Vector2`, `State`            |
| Functions        | lowercase        | `angle2d`, `dotprod`, `haskey`         |
| Word separation  | no separator (unless needed) | `isequal`, `indexin`  |
| Multi-word funcs | underscores when needed | `born_rule_constraint`  |
| Constants        | PascalCase       | `ZBasis`                               |
| Type parameters  | PascalCase       | `Vector{Scalar}`                       |
| Private helpers  | leading `_`      | `_internal_helper()`                   |
| Mutating funcs   | trailing `!`     | `sort!`, `push!`                       |

- Avoid abbreviations (`indexin` not `indxin`).
- Avoid single-letter names except for: `ψ` (quantum state),
  `α`, `β` (amplitudes), `θ`, `φ` (angles).
- If a function name needs multiple words, consider whether it
  represents more than one concept and should be split.

### Module Structure

- One module per file; filename matches module name.
- Explicit `export` statements at or near the top of the module.
- Do **not** indent the body of the module (standard Julia style).
- Relative imports for sibling modules: `using ..MathUtils`.
- Load only one module per `using`/`import` line.

```julia
module MathUtils

export Scalar, Angle, Vector2

const Scalar::DataType = AbstractFloat

struct Angle
    value::Real
end

end  # module MathUtils
```

### Formatting

- **Indentation**: 4 spaces (no tabs).
- **Line length**: max 92 characters.
- **Trailing whitespace**: avoid.
- **Blank lines**: two between function definitions;
  one between logical blocks within a function.
- **Parentheses**: no space before `(`, space after for multi-arg calls.
- **Binary operators**: surround with space, e.g. `a + b`.
- **Brackets**: no space inside, e.g. `string(1, 2)` not `string( 1 , 2 )`.
- **Type annotations**: use `::Type` for public function return types.
- **Floats**: do not omit zeros (`1.0` not `1.`, `.1` not `0.1` unless needed).
- **Unicode operators**: prefer ASCII operators when possible.

```julia
# Good
function angle2d(w::Vector{Scalar}, transform::Function)::Angle
    return transform(atand(y(w), x(w)))
end

# Avoid
function angle2d ( w :: Vector , transform :: Function )
    return transform(atand(y(w), x(w)))
end
```

### Type Annotations

- Annotate function arguments with types.
- Annotate return types for public functions.
- Use parametric types: `Vector{Scalar}` not `Vector`.
- Use `const` for immutable module-level values.
- Avoid global variables; pass state explicitly.

```julia
const ZBasis = Basis([1, 0], [0, 1])

function dotprod(w::Vector{Scalar}, v::Vector{Scalar})::Scalar
    return sum(w .* v)
end
```

### Error Handling

- Use `ErrorException` for general errors.
- Use `DomainError` for invalid domain values.
- Include values in messages: `"Vector Must Be Size 2, Found Size $(length(w))"`.
- Validate early in constructors.

```julia
function Vector2(w::Vector)
    if length(w) != 2
        throw(ErrorException("Vector2 Must be Length 2"))
    end
    return new(w[1], w[2])
end
```

### Control Flow

- Use `begin`/`end` blocks for multi-line expressions.
- Prefer `in` over `=` or `∈` in `for` loops: `for i in 1:n`.
- Keep branches balanced; extract to helper functions if unbalanced.

```julia
Base.getindex(w::Vector2, i::Int) = begin
    if i == 1
        return w.x
    elseif i == 2
        return w.y
    else
        throw(ErrorException("Index Out of Range $i"))
    end
end
```

### Documentation

- Add docstrings to **all exported functions**, types, and constants.
- Document struct fields with comments.
- Document type parameters.

```julia
"""
    State(α::Real, β::Real)

Represents a quantum state with amplitudes α and β.
Must satisfy Born rule: |α|² + |β|² = 1.
"""
struct State
    α::Scalar
    β::Scalar
end

"""
    vector(ψ::State, basis::Basis=ZBasis)

Return the state vector of `ψ` in `basis`.
"""
function vector(ψ::State, basis::Basis=ZBasis)::Vector{Scalar}
    return ψ.α * basis[1] + ψ.β * basis[2]
end
```

### Testing

- Test file location: `test/runtests.jl`.
- Use `@testset` for grouping related tests.
- Test error conditions with `@test_throws`.
- Test edge cases and boundary conditions.
- Group related imports in a single `using` block, one module per line.

```julia
using Test

@testset "Vector2" begin
    @test_throws ErrorException Vector2([1, 2, 3])
    @test Vector2([0.6, 0.8]).x ≈ 0.6
end
```

### Performance Notes

- Use `@inbounds` only when bounds are guaranteed.
- Use `const` for compile-time constants.
- Prefer in-place operations for large vectors.
- Benchmark before optimizing (use BenchmarkTools.jl).
- Use `@view` to avoid copying when working with slices.

---

## Project Structure

```
QSimPrototype/
├── Project.toml          # Package manifest
├── Manifest.toml         # Dependency lockfile (do not edit manually)
├── src/
│   ├── QSim.jl           # Main module, re-exports public API
│   ├── Utils.jl          # MathUtils submodule (Angle, Vector2, etc.)
│   └── quantum/
│       └── Quantum.jl    # Quantum submodule (State, Basis, etc.)
└── test/
    └── runtests.jl       # Test entry point
```

### Adding Test Dependencies

Declare test-only dependencies in `Project.toml`:

```toml
[extras]
Test = "8dfed614-e22c-5e08-85e1-65c5234f0b40"

[targets]
test = ["Test"]
```

For larger projects, use the workspace pattern with `test/Project.toml`.

---

## Key Dependencies

- **LinearAlgebra**: vector/matrix operations.
- **Test**: unit testing framework (standard library).

---

## Conventions

- Quantum states: `State` struct with `α`, `β` amplitudes.
- Polar angle of state via `state_angle()` (renamed to avoid conflict with `Base.angle`).
- Bloch sphere angles via `bloch_angle()`.
- Born rule constraint: `born_rule_constraint()`.
- Ket notation for display: `|ψ⟩`.
- Z-basis is the default: `ZBasis = Basis([1, 0], [0, 1])`.

---

## Compatibility

- Follow [Semantic Versioning](https://semver.org/): breaking changes
  increment major version, new features increment minor, patches increment patch.
- Specify dependency compatibility bounds in the `[compat]` section
  of `Project.toml`.
- Avoid using `Julia` in package names (the `.jl` extension communicates this).