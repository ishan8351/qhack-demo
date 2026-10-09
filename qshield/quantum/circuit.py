from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import numpy as np

def build_shor_qiskit_circuit(N: int = 15, a: int = 7) -> QuantumCircuit:
    """
    Constructs a runnable pedagogical QuantumCircuit for Shor's order finding on N=15 with base a=7.
    Uses 4 counting qubits (Register 1) and 4 work qubits (Register 2).
    """
    # 4 counting qubits + 4 auxiliary work qubits
    q_count = QuantumRegister(4, name='count')
    q_work = QuantumRegister(4, name='work')
    c_reg = ClassicalRegister(4, name='meas')
    qc = QuantumCircuit(q_count, q_work, c_reg)

    # Initialize work register to |1> (0001)
    qc.x(q_work[0])

    # Apply Hadamard gates to counting register to create superposition
    for q in q_count:
        qc.h(q)

    # Controlled modular multiplication: a=7 mod 15
    # 7^1 mod 15 = 7: SWAP work[0], work[1]; SWAP work[1], work[2]
    qc.cx(q_count[0], q_work[1])
    qc.cx(q_count[0], q_work[2])

    # 7^2 mod 15 = 4
    qc.cx(q_count[1], q_work[2])

    # 7^4 mod 15 = 1 (Identity)
    qc.barrier()

    # Inverse Quantum Fourier Transform (IQFT) on counting register
    for i in range(4):
        for j in range(i):
            qc.cp(-np.pi / float(2**(i - j)), q_count[j], q_count[i])
        qc.h(q_count[i])

    qc.barrier()
    qc.measure(q_count, c_reg)

    return qc
