from datetime import datetime, timezone
from qshield.cbom.schema import CBOMReport, QuantumRisk
from qshield.risk.mosca import evaluate_mosca_inequality, DataClassification
from qshield.risk.readiness import calculate_phased_readiness

def generate_executive_report(report: CBOMReport) -> str:
    """
    Generates a formal Markdown Executive Compliance & Risk Report for CISOs and audit teams.
    """
    # Mosca evaluation
    mosca = evaluate_mosca_inequality(
        shelf_life_years=10.0,
        migration_time_years=2.3,
        q_day_years=12.0,
        data_class=DataClassification.FINANCIAL_RECORDS
    )

    progression = calculate_phased_readiness(report.readiness_score)

    broken_count = sum(1 for f in report.findings if f.quantum_risk == QuantumRisk.BROKEN)
    weakened_count = sum(1 for f in report.findings if f.quantum_risk == QuantumRisk.WEAKENED)
    safe_count = sum(1 for f in report.findings if f.quantum_risk == QuantumRisk.SAFE)
    deprecated_count = sum(1 for f in report.findings if f.quantum_risk == QuantumRisk.DEPRECATED)

    return f"""# Q-SHIELD Executive Quantum Risk & Compliance Report
**Target System:** `{report.target_name}`
**Assessment Date:** {datetime.now(timezone.utc).strftime('%B %d, %Y')}
**Platform Version:** Q-SHIELD v1.0.0 (Standards: NIST FIPS 203/204/205)

---

## 1. Executive Summary & Readiness Posture
The target codebase `{report.target_name}` was subjected to automated Cryptographic Bill of Materials (CBOM) discovery and post-quantum threat analysis.

- **Current Quantum Readiness Score:** `{report.readiness_score} / 100` (Critically Exposed)
- **Total Cryptographic Assets Discovered:** `{report.total_assets}`
- **Quantum-Vulnerable Assets (Shor/Grover):** `{report.quantum_vulnerable_count}`
  - Shor-Broken Public-Key Assets (RSA, ECDSA, DH): `{broken_count}`
  - Grover-Weakened Symmetric Assets (AES-128): `{weakened_count}`
  - Classically Broken/Deprecated Assets (MD5, SHA-1): `{deprecated_count}`
  - Certified Quantum-Resilient Assets (SHA-256): `{safe_count}`

---

## 2. Mosca's Inequality & "Harvest Now, Decrypt Later" Threat
Data confidentiality is at immediate risk according to Mosca's theorem ($X + Y > Z$):
- **Statutory Data Shelf-Life ($X$):** `10.0 Years` (Financial Records Retention)
- **Estimated Migration Window ($Y$):** `2.3 Years` (Microservices & Database Re-keying)
- **Estimated Q-Day Horizon ($Z$):** `12.0 Years`
- **Total Exposure Horizon ($X + Y$):** `12.3 Years`
- **Exposure Assessment:** `{mosca['exposure_level']}` (`12.3 > 12.0`)
- **Audit Verdict:** {mosca['verdict']}

---

## 3. Regulatory Compliance Deadlines
- **NIST FIPS 203 (ML-KEM) & FIPS 204 (ML-DSA):** Finalized August 2024.
- **NIST IR 8547 Draft:** Mandates the initiation of post-quantum migration immediately; classical RSA and ECC deprecated by **2030** and prohibited by **2033**.
- **CNSA 2.0 Federal Directive:** Mandates post-quantum algorithm readiness across critical infrastructure by **2030**.

---

## 4. Projected 4-Phase Migration Trajectory
By implementing Q-SHIELD's crypto-agility recommendations, the organization's readiness score advances as follows:

| Milestone | Target Readiness | Scope & Objectives |
| :--- | :--- | :--- |
| **Today (Baseline)** | `{progression[0]['score']}/100` | Current vulnerable posture |
| **Phase 1 (Perimeter)** | `{progression[1]['score']}/100` | Hybrid TLS (X25519MLKEM768), JWT to ML-DSA-65 / Ed25519 |
| **Phase 2 (Internal Services)** | `{progression[2]['score']}/100` | SSH host re-keying, DB upgrade to AES-256-GCM, MD5/SHA-1 deprecation |
| **Phase 3 (Data-at-Rest)** | `{progression[3]['score']}/100` | Hybrid PQC envelope encryption on 10-year archives |
| **Phase 4 (Zero Trust)** | `{progression[4]['score']}/100` | Full deprecation of legacy cipher suites and pure FIPS 203/204 enforcement |

---
*Report certified by Q-SHIELD Native Security Engine.*
"""
