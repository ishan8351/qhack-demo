import pytest
from qshield.risk.mosca import evaluate_mosca_inequality, DataClassification
from qshield.risk.grover import evaluate_grover_degradation
from qshield.risk.readiness import calculate_phased_readiness

def test_mosca_inequality_quantumbank():
    """Verify Mosca's inequality calculation on QuantumBank payment-api (10 + 2.3 > 12)."""
    result = evaluate_mosca_inequality(
        shelf_life_years=10.0,
        migration_time_years=2.3,
        q_day_years=12.0,
        data_class=DataClassification.FINANCIAL_RECORDS
    )
    assert result["is_at_risk"] is True
    assert result["exposure_level"] == "HIGH"
    assert result["total_risk_horizon"] == 12.3
    assert result["margin_years"] == 0.3
    assert "outlive their encryption" in result["verdict"].lower()

def test_mosca_inequality_low_risk():
    """Verify Mosca calculation for short-lived data."""
    result = evaluate_mosca_inequality(
        shelf_life_years=1.0,
        migration_time_years=1.0,
        q_day_years=12.0,
        data_class=DataClassification.TRANSIENT_SESSION
    )
    assert result["is_at_risk"] is False
    assert result["exposure_level"] == "LOW"
    assert result["margin_years"] == -10.0

def test_grover_degradation():
    """Verify Grover brute-force key strength degradation."""
    aes128 = evaluate_grover_degradation("AES-128", 128)
    assert aes128["classical_bits"] == 128
    assert aes128["effective_quantum_bits"] == 64
    assert aes128["status"] == "WEAKENED"
    assert aes128["quantum_safe"] is False

    aes256 = evaluate_grover_degradation("AES-256", 256)
    assert aes256["classical_bits"] == 256
    assert aes256["effective_quantum_bits"] == 128
    assert aes256["status"] == "QUANTUM_RESILIENT"
    assert aes256["quantum_safe"] is True

def test_phased_readiness_progression():
    """Verify readiness progression matching Slide 8: 33 -> 42 -> 55 -> 84 -> 96."""
    progression = calculate_phased_readiness(baseline_score=33.0)
    assert progression[0]["phase"] == "Today"
    assert progression[0]["score"] == 33.0

    assert progression[1]["phase"] == "Phase 1"
    assert progression[1]["score"] == 42.0

    assert progression[2]["phase"] == "Phase 2"
    assert progression[2]["score"] == 55.0

    assert progression[3]["phase"] == "Phase 3"
    assert progression[3]["score"] == 84.0

    assert progression[4]["phase"] == "Phase 4"
    assert progression[4]["score"] == 96.0
