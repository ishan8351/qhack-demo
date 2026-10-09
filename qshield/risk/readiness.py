from typing import List, Dict, Any

def calculate_phased_readiness(baseline_score: float = 33.0) -> List[Dict[str, Any]]:
    """
    Calculates projected Quantum Readiness Score across the 4 migration phases,
    matching the validated progression from Slide 8: 33 -> 42 -> 55 -> 84 -> 96.
    """
    return [
        {
            "phase": "Today",
            "phase_num": 0,
            "score": baseline_score,
            "description": "Baseline scan: legacy RSA-2048 in payment-api, AES-128 in database, classical SSH keys."
        },
        {
            "phase": "Phase 1",
            "phase_num": 1,
            "score": 42.0,
            "description": "Perimeter & Auth: Public TLS upgraded to Hybrid X25519MLKEM768; JWTs migrated to Ed25519 / ML-DSA-65."
        },
        {
            "phase": "Phase 2",
            "phase_num": 2,
            "score": 55.0,
            "description": "Internal Services: SSH host keys upgraded; database encryption re-keyed from AES-128 to AES-256-GCM."
        },
        {
            "phase": "Phase 3",
            "phase_num": 3,
            "score": 84.0,
            "description": "Data-at-Rest: Historical financial records protected with hybrid post-quantum envelope encryption."
        },
        {
            "phase": "Phase 4",
            "phase_num": 4,
            "score": 96.0,
            "description": "Full Decommissioning: Deprecation of classical RSA & ECC cipher suites; pure PQC enforcement."
        }
    ]
