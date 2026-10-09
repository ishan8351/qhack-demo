import math
from typing import Dict, Any

def evaluate_grover_degradation(algorithm_name: str, key_bits: int) -> Dict[str, Any]:
    """
    Evaluates quadratic speedup degradation under Grover's search algorithm.
    Symmetric keys of n bits drop to effective security of n/2 bits: O(2^(n/2)).
    """
    effective_bits = key_bits // 2
    quantum_safe = effective_bits >= 128

    if effective_bits < 80:
        status = "WEAKENED"
        recommendation = "Insecure under quantum adversary. Upgrade immediately to AES-256."
    elif effective_bits < 128:
        status = "MARGINAL"
        recommendation = "Marginal quantum security. Deprecate in favor of 256-bit symmetric keys."
    else:
        status = "QUANTUM_RESILIENT"
        recommendation = "Certified quantum-safe symmetric key length (retains 128-bit security margin)."

    return {
        "algorithm": algorithm_name,
        "classical_bits": key_bits,
        "effective_quantum_bits": effective_bits,
        "speedup_factor": "Quadratic O(2^(n/2))",
        "quantum_safe": quantum_safe,
        "status": status,
        "recommendation": recommendation
    }
