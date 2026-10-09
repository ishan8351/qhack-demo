import uuid
from typing import Dict, Any
from datetime import datetime, timezone
from qshield.cbom.schema import CBOMReport, AssetType, QuantumRisk

def export_cyclonedx_1_6(report: CBOMReport) -> Dict[str, Any]:
    """
    Exports a CBOMReport into official CycloneDX 1.6 Cryptographic Bill of Materials JSON.
    Conforms to the cryptographic-asset schema and cryptoProperties specification.
    """
    components = []
    for f in report.findings:
        primitive = "asymmetric"
        if "AES" in f.algorithm:
            primitive = "symmetric"
        elif any(h in f.algorithm for h in ["SHA", "MD5"]):
            primitive = "hash"
        elif "TLS" in f.algorithm or "SSH" in f.algorithm or "JWT" in f.algorithm:
            primitive = "protocol"

        comp = {
            "type": "cryptographic-asset",
            "name": f.algorithm,
            "bom-ref": f.id,
            "version": "1.0",
            "description": f.description,
            "evidence": {
                "occurrences": [
                    {
                        "location": f.file_path,
                        "line": f.line_number,
                        "offset": 0,
                        "symbol": f.code_snippet
                    }
                ]
            },
            "cryptoProperties": {
                "assetType": f.asset_type.value,
                "algorithmProperties": {
                    "primitive": primitive,
                    "parameterSetIdentifier": f.algorithm,
                    "classicalSecurityLevel": 128 if "AES-128" in f.algorithm else (256 if "256" in f.algorithm else 112)
                },
                "quantumRisk": f.quantum_risk.value,
                "quantumSecurityLevel": 0 if f.quantum_risk == QuantumRisk.BROKEN else (64 if f.quantum_risk == QuantumRisk.WEAKENED else 128),
                "severity": f.severity.value,
                "recommendedReplacement": f.recommended_replacement,
                "roadmapPhase": f.phase
            }
        }
        components.append(comp)

    return {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "version": 1,
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tools": {
                "components": [
                    {
                        "type": "application",
                        "name": "Q-SHIELD",
                        "version": "1.0.0",
                        "description": "End-to-End Quantum Security Platform"
                    }
                ]
            },
            "component": {
                "type": "application",
                "name": report.target_name,
                "description": f"Target codebase analyzed by Q-SHIELD (Readiness: {report.readiness_score}/100)"
            }
        },
        "components": components
    }
