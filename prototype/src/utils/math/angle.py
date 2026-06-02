from dataclasses import dataclass


@dataclass(frozen=True)
class Angle:
    value: float

    def __post_init__(self):
        super().__setattr__("value", self.value % 360)

    def __repr__(self) -> str:
        return f"{self.value}\u00b0"
