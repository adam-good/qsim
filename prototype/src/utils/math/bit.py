from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class Bit:
    """Immutable binary digit constrained to values 0 or 1.
    
    Supports interoperability with int and bool while maintaining
    strict value constraints. Only accepts int or bool types.
    
    Examples:
        >>> bit_zero = Bit(0)
        >>> bit_one = Bit(1)
        >>> Bit(True)  # True coerces to 1
        Bit(value=1)
    """
    
    value: int
    
    def __post_init__(self) -> None:
        """Validate that value is exactly 0 or 1 after initialization."""
        if not isinstance(self.value, (int, bool)):
            raise ValueError(
                f"Bit must be 0 or 1, got {self.value!r}"
            )
        normalized = int(self.value)
        if normalized not in (0, 1):
            raise ValueError(
                f"Bit must be 0 or 1, got {self.value!r}"
            )
        object.__setattr__(self, "value", normalized)
    
    def __int__(self) -> int:
        """Convert to integer (0 or 1)."""
        return self.value
    
    def __bool__(self) -> bool:
        """Convert to boolean (False for 0, True for 1)."""
        return bool(self.value)
    
    def __index__(self) -> int:
        """Support use as sequence index."""
        return self.value
    
    def __add__(self, other: object) -> int:
        """Addition modulo 2 (XOR behavior for bits).
        
        >>> Bit(0) + Bit(0)
        0
        >>> Bit(0) + Bit(1)
        1
        >>> Bit(1) + Bit(1)
        0
        """
        if isinstance(other, Bit):
            return (self.value + other.value) % 2
        if isinstance(other, int):
            return (self.value + other) % 2
        return NotImplemented
    
    def __radd__(self, other: int) -> int:
        return self.__add__(other)
    
    def __mul__(self, other: object) -> int:
        """Multiplication modulo 2 (AND behavior for bits).
        
        >>> Bit(0) * Bit(0)
        0
        >>> Bit(0) * Bit(1)
        0
        >>> Bit(1) * Bit(1)
        1
        """
        if isinstance(other, Bit):
            return (self.value * other.value) % 2
        if isinstance(other, int):
            return (self.value * other) % 2
        return NotImplemented
    
    def __rmul__(self, other: int) -> int:
        return self.__mul__(other)
    
    def __neg__(self) -> int:
        """Negation modulo 2 (identity for bits: -0 = 0, -1 = 1 in mod 2)."""
        return self.value
    
    def __pos__(self) -> int:
        """Unary + is identity."""
        return self.value
    
    def __and__(self, other: object) -> bool:
        """Logical AND."""
        if isinstance(other, (Bit, int, bool)):
            return bool(self) and bool(other)
        return NotImplemented
    
    def __rand__(self, other: int) -> bool:
        return bool(other) and bool(self)
    
    def __or__(self, other: object) -> bool:
        """Logical OR."""
        if isinstance(other, (Bit, int, bool)):
            return bool(self) or bool(other)
        return NotImplemented
    
    def __ror__(self, other: int) -> bool:
        return bool(other) or bool(self)
    
    def __xor__(self, other: object) -> bool:
        """Logical XOR."""
        if isinstance(other, (Bit, int, bool)):
            return bool(self) != bool(other)
        return NotImplemented
    
    def __rxor__(self, other: int) -> bool:
        return bool(other) != bool(self)
    
    def __invert__(self) -> int:
        """Logical NOT (0 → 1, 1 → 0)."""
        return 1 - self.value
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison."""
        if isinstance(other, Bit):
            return self.value == other.value
        if isinstance(other, (int, bool)):
            return self.value == int(other)
        return NotImplemented
    
    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.value)
    
    def __lt__(self, other: object) -> bool:
        """Less-than comparison."""
        if isinstance(other, Bit):
            return self.value < other.value
        if isinstance(other, (int, bool)):
            return self.value < int(other)
        return NotImplemented
    
    def __le__(self, other: object) -> bool:
        if isinstance(other, Bit):
            return self.value <= other.value
        if isinstance(other, (int, bool)):
            return self.value <= int(other)
        return NotImplemented
    
    def __gt__(self, other: object) -> bool:
        if isinstance(other, Bit):
            return self.value > other.value
        if isinstance(other, (int, bool)):
            return self.value > int(other)
        return NotImplemented
    
    def __ge__(self, other: object) -> bool:
        if isinstance(other, Bit):
            return self.value >= other.value
        if isinstance(other, (int, bool)):
            return self.value >= int(other)
        return NotImplemented
    
    def __repr__(self) -> str:
        return f"Bit(value={self.value})"


BIT_0: Final[Bit] = Bit.__new__(Bit)
object.__setattr__(BIT_0, "value", 0)

BIT_1: Final[Bit] = Bit.__new__(Bit)
object.__setattr__(BIT_1, "value", 1)