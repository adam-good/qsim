from src.quantum.algorithms.bb84 import BB84BasisReciever, BB84BasisTransmitter, BB84BasisPair
import quantum.algorithms.random as qrand
import quantum.algorithms.bb84 as bb84
import quantum.device as qdev
import utils.channel as chnl
import utils.math.bit as bit
import threading
KEY_SIZE = 2**0

def send_key(
    config: bb84.BB84Config,
    device: qdev.QuantumDevice,
    quant_send: chnl.Channel[qdev.Qubit],
    auth_send: chnl.Channel[bb84.BB84Basis],
    auth_recv: chnl.Channel[bb84.BB84Basis]
) -> bb84.BB84Result:
    def gen_key(device: qdev.QuantumDevice, n: int) -> list[bit.Bit]:
        return [qrand.random_bit(device) for _ in range(n)]
    def gen_basis(device: qdev.QuantumDevice, n: int) -> list[bb84.BB84Basis]:
        return [bb84.BB84Basis(qrand.random_bit(device)) for _ in range(n)]

    result: list[bb84.BB84Result] = [bb84.BB84Result(False) for _ in range(KEY_SIZE)]
    key = gen_key(device, KEY_SIZE)
    basises = gen_basis(device, KEY_SIZE)
    for i,(key_bit,basis) in enumerate(zip(key, basises)):
        with device.alloc_single() as qubit:
            encoder = bb84.BB84Encoder(config, device, qubit, bb84.BasisBitPair(basis,key_bit))
            encoding = bb84.bb84_encode(encoder)
            transmitter = bb84.BB84QuantumTransmitter(device, quant_send, encoding)
            _ = bb84.bb84_transmit_qubit(transmitter)
        
        reciever = BB84BasisReciever(auth_recv)
        remote_basis, _ = bb84.bb84_recv_basis(reciever)

        transmitter = bb84.BB84BasisTransmitter(auth_send, basis)
        _ = bb84.bb84_transmit_basis(transmitter)

        basis_pair = bb84.BB84BasisPair(remote_basis, basis)
        result[i] = bb84.bb84_validate(basis_pair)

    return bb84.BB84Result(all(result))
  

def recv_key(
    device: qdev.QuantumDevice,
    quant_recv: chnl.Channel[qdev.Qubit],
    auth_send: chnl.Channel[bb84.BB84Basis],
    auth_recv: chnl.Channel[bb84.BB84Basis]
):
    def gen_basis(device: qdev.QuantumDevice, n: int) -> list[bb84.BB84Basis]:
        return [bb84.BB84Basis(qrand.random_bit(device)) for _ in range(n)]
    result: list[bb84.BB84Result] = [bb84.BB84Result(False) for _ in range(KEY_SIZE)]
    key: list[bit.Bit | None] = [None] * KEY_SIZE
    basises = gen_basis(device, KEY_SIZE)

    for i,basis in enumerate(basises):
        qubit_reciever = bb84.BB84QuantumReciever(device, quant_recv)
        qubit, qubit_reciever = bb84.bb84_recieve_qubit(qubit_reciever)

        pair = bb84.BasisQubitPair(basis, qubit)
        decoder = bb84.BB84Decoder(config, device, pair)
        decoding = bb84.bb84_decode(decoder)

        basis_transmitter = bb84.BB84BasisTransmitter(auth_send, basis)
        basis_transmitter = bb84.bb84_transmit_basis(basis_transmitter)

        basis_reciever = bb84.BB84BasisReciever(auth_recv)
        remote_basis, basis_reciever = bb84.bb84_recv_basis(basis_reciever)

        basis_pair = BB84BasisPair(remote_basis, basis)
        result[i] = bb84.bb84_validate(basis_pair)
        if result[i] == bb84.BB84Result(True):
            key[i] = decoding.bit

        

    

if __name__ == "__main__":
    device1 = qdev.QuantumDevice([qdev.Qubit(0)])
    device2 = qdev.QuantumDevice([qdev.Qubit(1)])
    # auth_channel: chnl.Channel[bb84.BB84Basis] = chnl.Channel[bb84.BB84Basis]()

    n_bits = 2**0
    key: list[bit.Bit] = [qrand.random_bit(device1) for _ in range(n_bits)]
    print(f"Key:  {''.join([str(k) for k in key])}")


    config = bb84.BB84Config()
    for k in key:
        basis: bb84.BB84Basis = bb84.BB84Basis(qrand.random_bit(device1))
        with device1.alloc_single() as qubit:
            encoder = bb84.BB84Encoder(config, device1, qubit, bb84.BasisBitPair(basis, key[0]))
            encoding = bb84.bb84_encode(encoder)
            
            transmitter = bb84.BB84QuantumTransmitter(device1, chnl.Channel[qdev.Qubit](), encoding)
            transmission = bb84.bb84_transmit_qubit(transmitter)
    
        reciever = bb84.BB84QuantumReciever(device2, transmission.channel)
        qubit, reciever = bb84.bb84_recieve_qubit(reciever)
        if qubit is None:
            raise ValueError("Recieved None Qubit! Uh Oh!")
    
        basis = bb84.BB84Basis(qrand.random_bit(device2))
        decoder = bb84.BB84Decoder(config, device2, bb84.BasisQubitPair(basis, qubit))
        decoding = bb84.bb84_decode(decoder)

    

    

