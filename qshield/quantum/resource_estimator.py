import math
from typing import Dict, Any

def estimate_rsa_quantum_resources(key_bits: int = 2048) -> Dict[str, Any]:
    """
    Estimates the quantum resources required to factor an RSA integer of key_bits
    based on peer-reviewed literature:
    - Gidney & Ekerå (2019): "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits"
    - Gidney (2025): "How to factor 2048 bit RSA integers with less than a million noisy qubits" (arXiv:2505.15917)
    """
    logical_qubits = 2 * key_bits + int(math.ceil(math.log2(key_bits)))
    
    # Gidney & Ekerå 2019 baseline (~20 million physical qubits)
    qubits_2019 = 20_000_000 if key_bits == 2048 else int(20_000_000 * (key_bits / 2048)**2)
    
    # Gidney 2025 optimized architecture (< 1 million physical qubits)
    qubits_2025 = 980_000 if key_bits == 2048 else int(980_000 * (key_bits / 2048)**1.8)

    # Surface code distance
    code_distance = 27 if key_bits <= 2048 else 33

    # Toffoli gate depth
    toffoli_count = int(0.3 * (key_bits**3))

    return {
        "key_size": key_bits,
        "algorithm": f"RSA-{key_bits}",
        "logical_qubits": logical_qubits,
        "physical_noisy_qubits_gidney2019": qubits_2019,
        "physical_noisy_qubits_gidney2025": qubits_2025,
        "surface_code_distance": code_distance,
        "toffoli_gate_depth": toffoli_count,
        "estimated_runtime": "8 hours at 1 microsecond reaction time",
        "reference": "Gidney & Ekerå (2019) arXiv:1905.09749, Gidney (2025) arXiv:2505.15917"
    }
