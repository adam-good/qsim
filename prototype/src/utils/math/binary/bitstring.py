import dataclasses
from utils.math.binary import bit

@dataclasses.dataclass(frozen=True)
class Bitstring:
    bits: tuple[bit.Bit, ...]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Bitstring):
            return self.bits == other.bits
        else:
            return NotImplemented

    def __repr__(self):
        return "".join(f"b{int(b)}" for b in self.bits)
    
