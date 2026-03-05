from string import ascii_lowercase
import typing
from typing import Iterator
from decorator import contextmanager
from enum import Enum
from quantum.qubit import Qubit
from quantum.state import QuantumState

class AllocState(Enum):
    ALLOCATED = 1
    FREE = 2    

class DeviceQubit():
    def __init__(self, label: str | None = None, log: typing.IO | None = None):
        self._label: str | None = label
        self.log = log
        self.qubit: Qubit = Qubit(label=label, log=True if log else False)
        self.status = AllocState.FREE

    @property
    def label(self) -> str:
        return self._label if self._label else ""

    def alloc(self) -> Qubit:
        self.status = AllocState.ALLOCATED
        return self.qubit

    def dealloc(self):
        self.qubit = self.qubit.reset()
        self.status = AllocState.FREE

class QuantumDevice():
    def __init__(self, n: int, var_names: list[str] = list(ascii_lowercase), log: typing.IO | None = None, visualize: bool = False):
        self.n_qubits = n
        self.log = log
        self.qubits: list[DeviceQubit] = [DeviceQubit(label=var_names[i], log=self.log) for i in range(n)]

    def _alloc(self) -> Qubit:
        for d_qubit in self.qubits:
            if d_qubit.status == AllocState.FREE:
                return d_qubit.alloc()
        else:
            raise Exception("You're out of Qubits, Buddy!")

    def _dealloc(self, qubit: Qubit):
        for d_qubit in self.qubits:
            if qubit is d_qubit.qubit:
                d_qubit.dealloc()
                break
            else:
                raise Exception("WOOP WOOP !Foriegn Qubit Detected! WOOP WOOP")

    @property
    def history(self) -> dict[str, list[QuantumState]]:
        if self.log:
            return {qubit.label:qubit.qubit.history for qubit in self.qubits if qubit.qubit.history}
        else:
            raise Exception("Device Not Recording State History!")

    @contextmanager
    def qalloc(self) -> Iterator[Qubit]:
        try:
            qubit = self._alloc()
            yield qubit
        finally:
            self._dealloc(qubit)
            
