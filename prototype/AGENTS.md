# AGENTS.md - qsim/prototype

## Project Overview
Pure-Python quantum computing simulator (Python 3.14+). No external runtime dependencies — no numpy/scipy. Implements math primitives (Vector, Matrix), quantum states, gates, device abstraction, and a QRNG algorithm.

## Commands

### Run all tests
```
uv run python -m unittest discover -s tests
```

### Run a single test file
```
uv run python -m unittest tests/quantum/test_state.py
```

### Run a single test class or method
```
uv run python -m unittest tests.quantum.test_state.TestQuantumState.test_quantumstate_angles
```

### Run an example
```
uv run python examples/example_quantum_state.py
```

### Lint / format with ruff
```
uv run ruff check .          # lint
uv run ruff format .         # format
uv run ruff check --fix .    # lint + auto-fix
```

### Type check with ty
```
uv run ty check
```

### Add a dependency
```
uv add <package>
uv add --dev <package>       # dev dependency
```

## Code Style

### Imports
- **Absolute imports only** — no relative imports (`from . import ...`)
- `quantum.*` modules: use `import quantum.state as qstate` alias pattern
- `utils.math.*` modules: use `from utils.math.vector import Vector` pattern
- Never use `from module import *`

### Formatting
- 4-space indentation
- Ruff handles formatting — run `uv run ruff format .` before committing
- Keep lines short; no hard limit enforced but stay reasonable

### Types
- Use modern `list[...]`, `dict[...]`, `tuple[...]` syntax (Python 3.9+), not `List[...]`/`Dict[...]`
- Use `X | Y` union syntax, not `Union[X, Y]`
- `Scalar` is a `TypeAlias = float` — use it instead of bare `float` for quantum amplitudes
- Type aliases for domain types: `QState = Vector`, `QGate = Matrix`
- Annotate function parameters and return types; be thorough on public APIs
- Use `object` for `__eq__` parameter type (per PEP 484)

### Naming
- Classes: `PascalCase` — `Vector`, `Matrix`, `SimQubit`, `SimDevice`
- Functions: `snake_case` — `hadamard`, `negate`, `collapse`, `probability`
- Constants: `UPPER_SNAKE_CASE` — `KET0`, `KET1`, `Z_BASIS`, `COMMON_GATES`
- Private methods: leading underscore — `_alloc`, `_n_alloc`, `_elementwise_op`
- Module aliases: `qstate`, `qgate`, `qsim`, `qdev`

### Dataclasses
- Use `@dataclass(frozen=True)` for immutable math types (`Vector`, `Matrix`)
- Regular classes for mutable state (`SimQubit`, `SimDevice`)

### Error Handling
- `raise NotImplementedError()` for unsupported types in operator overloads
- `raise Exception("message")` for domain errors (non-unitary gates, dimension mismatches)
- `assert` for internal invariants (e.g., allocation bounds)
- No custom exception classes defined yet
- No `try/except` in source code (only `try/finally` for context manager cleanup)

### Testing
- **Framework: `unittest`** (stdlib) — no pytest
- Test classes inherit from `unittest.TestCase`
- Assertions: `self.assertEqual()`, `self.assertAlmostEqual()`, `self.assertIs()`, `self.assertRaises()`
- Test file naming: `test_*.py` mirroring `src/` directory structure
- Test class naming: `Test<ModuleName>` (e.g., `TestQuantumState`)
- Test method naming: `test_<module>_<feature>` (e.g., `test_quantumstate_angles`)
- Empty test files are valid placeholders for future tests

### Architecture
```
src/
  utils/math/       — Scalar, Vector, Matrix, helper_funcs
  quantum/          — state, gate, device (ABC), simulation (concrete)
  quantum/algorithms/ — qrng
tests/              — mirrors src/ structure
examples/           — runnable demos
```
