import pytest
from qshield.quantum.shor import ShorSimulator
from qshield.quantum.resource_estimator import estimate_rsa_quantum_resources

def test_shor_factoring_all_moduli():
    """Verify Shor's statevector algorithm factors 15, 21, 143, 221, and 247."""
    simulator = ShorSimulator()
    targets = [
        (15, {3, 5}),
        (21, {3, 7}),
        (143, {11, 13}),
        (221, {13, 17}),
        (247, {13, 19})
    ]
    for N, expected_factors in targets:
        result = simulator.factor(N)
        assert result["success"] is True, f"Failed to factor N={N}"
        factors = {result["factor_1"], result["factor_2"]}
        assert factors == expected_factors, f"N={N}: Expected {expected_factors}, got {factors}"

def test_shor_interference_peaks_theory():
    """Verify N=15, a=7 produces exact peaks every Q/r = 64 matching Slide 5."""
    simulator = ShorSimulator()
    result = simulator.simulate_period_finding(N=15, a=7)
    
    assert result["true_order_r"] == 4
    assert result["register_size_Q"] == 256
    assert result["peak_spacing"] == 64.0
    
    # Verify probability peaks at 0, 64, 128, 192
    peak_indices = result["peak_indices"]
    expected_peaks = [0, 64, 128, 192]
    assert peak_indices == expected_peaks
    
    # Peak probabilities should be approx 0.25 each
    for peak_idx in peak_indices:
        prob = result["probabilities"][peak_idx]
        assert abs(prob - 0.25) < 0.01, f"Peak {peak_idx} prob {prob} != 0.25"

def test_gidney_ekera_resource_estimator():
    """Verify physical quantum resource estimation for RSA-2048."""
    est = estimate_rsa_quantum_resources(key_bits=2048)
    assert est["key_size"] == 2048
    assert est["logical_qubits"] > 4000
    assert 500_000 <= est["physical_noisy_qubits_gidney2025"] <= 2_000_000
    assert est["physical_noisy_qubits_gidney2019"] >= 15_000_000
    assert "8 hours" in est["estimated_runtime"].lower()

def test_qiskit_circuit_generation():
    """Verify Qiskit quantum circuit construction for N=15 modular exponentiation."""
    from qshield.quantum.circuit import build_shor_qiskit_circuit
    circuit = build_shor_qiskit_circuit(N=15, a=7)
    assert circuit is not None
    assert circuit.num_qubits >= 4
    assert circuit.depth() > 0
