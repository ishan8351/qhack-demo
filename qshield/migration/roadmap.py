from typing import List, Dict, Any
from qshield.cbom.schema import CBOMReport, Finding

class CryptoAgilityRoadmap:
    """
    Orchestrates the 4-phase Post-Quantum Cryptography migration roadmap.
    Partitions cryptographic assets and tracks readiness score progression.
    """

    def __init__(self, report: CBOMReport):
        self.report = report

    def get_phases(self) -> List[Dict[str, Any]]:
        findings = self.report.findings
        
        # Partition findings by phase tag
        p1_findings = [f for f in findings if f.phase == 1]
        p2_findings = [f for f in findings if f.phase == 2]
        p3_findings = [f for f in findings if f.phase == 3]
        p4_findings = [f for f in findings if f.phase == 4]

        return [
            {
                "phase_num": 1,
                "title": "Phase 1: Perimeter & Authentication",
                "target_readiness": 42.0,
                "estimated_time": "3–6 Months",
                "description": "Upgrade external TLS endpoints to Hybrid X25519MLKEM768; migrate JWT RS256 to ML-DSA-65 or Ed25519; deploy WebCrypto hybrid KEM.",
                "findings": p1_findings,
                "count": len(p1_findings)
            },
            {
                "phase_num": 2,
                "title": "Phase 2: Internal Microservices & Storage",
                "target_readiness": 55.0,
                "estimated_time": "6–12 Months",
                "description": "Re-key internal SSH hosts to post-quantum key exchange (sntrup761/ML-KEM); upgrade database encryption from AES-128 to AES-256-GCM; deprecate MD5/SHA-1.",
                "findings": p2_findings,
                "count": len(p2_findings)
            },
            {
                "phase_num": 3,
                "title": "Phase 3: Data-at-Rest & Long-Lived Key Stores",
                "target_readiness": 84.0,
                "estimated_time": "12–18 Months",
                "description": "Implement hybrid PQC envelope encryption on customer databases holding 10-year financial records; migrate HSM and KMS keys to ML-KEM-768.",
                "findings": p3_findings,
                "count": len(p3_findings)
            },
            {
                "phase_num": 4,
                "title": "Phase 4: Full Decommissioning & Zero Trust",
                "target_readiness": 96.0,
                "estimated_time": "18–24 Months",
                "description": "Strict cipher-suite enforcement; disable legacy RSA-2048 and ECC fallbacks; complete transition to pure NIST FIPS 203/204/205.",
                "findings": p4_findings,
                "count": len(p4_findings)
            }
        ]
