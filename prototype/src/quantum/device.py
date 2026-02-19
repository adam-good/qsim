from typing import Iterator
from decorator import contextmanager
from enum import Enum
from quantum.qubit import Qubit
import quantum.qubit as q

class AllocState(Enum):
    ALLOCATED = 1
    FREE = 2    

class DeviceQubit():
    def __init__(self):
        self.qubit = q.Qubit()
        self.status = AllocState.FREE

    def alloc(self) -> q.Qubit:
        self.status = AllocState.ALLOCATED
        return self.qubit

    def dealloc(self):
        # TODO: Should I reset here?
        del self.qubit
        self.qubit = q.Qubit()
        self.status = AllocState.FREE

class QuantumDevice():
    def __init__(self, n: int):
        self.n_qubits = n
        self.qubits = [DeviceQubit() for _ in range(n)]
        
    def _alloc(self) -> Qubit:
        for d_qubit in self.qubits:
            if d_qubit.status == AllocState.FREE:
                return d_qubit.alloc()
        else:
            raise Exception("You're out of Qubits, Buddy!")

    def _dealloc(self, qubit: q.Qubit):
        for d_qubit in self.qubits:
            if qubit is d_qubit.qubit:
                d_qubit.dealloc()
                break
            else:
                raise Exception("WOOP WOOP !Foriegn Qubit Detected! WOOP WOOP")

    @contextmanager
    def qalloc(self) -> Iterator[Qubit]:
        try:
            qubit = self._alloc()
            yield qubit
        finally:
            self._dealloc(qubit)
            
