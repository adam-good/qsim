import quantum.state as qstate

def allocate_qubit() -> qstate.state:
    return qstate.ket0()

def deallocate_qubit(psi: qstate.state):
    del psi
