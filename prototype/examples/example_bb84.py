import quantum.algorithms.qrng as qrng
import quantum.algorithms.bb84 as bb84
import quantum.device as qdev
import quantum.simulation as qsim
import utils.channel as chnl
import threading

if __name__ == '__main__':
    
    device1 = qsim.SimDevice(1)
    device2 = qsim.SimDevice(1)
    q_channel: chnl.Channel[qdev.Qubit] = chnl.new_channel()
    auth_channel: chnl.Channel[int] = chnl.new_channel()

    qend_a, qend_b = chnl.get_endpoints(q_channel)
    end_a, end_b = chnl.get_endpoints(auth_channel)
    
    n_bits = 2**4
    key: list[int] = [qrng.qrng(device1) for _ in range(n_bits)]
    print(f"Key:  {key}")

    sender = threading.Thread(target=bb84.bb84_send, args=(device1, key, len(key), qend_a, end_a))
    reciever = threading.Thread(target=bb84.bb84_recv, args=(device2, n_bits, qend_b, end_b,), kwargs={"verbose":True})

    sender.start()
    reciever.start()

    sender.join(timeout=5)
    reciever.join(timeout=5)
