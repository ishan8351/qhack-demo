from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AssetType(str, Enum):
    ALGORITHM = "algorithm"
    PROTOCOL = "protocol"
    CERTIFICATE = "certificate"
    KEY = "key"

class QuantumRisk(str, Enum):
    BROKEN = "BROKEN_BY_SHOR"          # RSA, ECC, DH
    WEAKENED = "WEAKENED_BY_GROVER"    # AES-128
    SAFE = "QUANTUM_RESILIENT"         # AES-256, ML-KEM, ML-DSA
    DEPRECATED = "CLASSICALLY_BROKEN"  # MD5, SHA-1, DES

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Finding(BaseModel):
    id: str = Field(..., description="Unique finding identifier, e.g. FIND-001")
    file_path: str
    line_number: int
    code_snippet: str
    algorithm: str
    asset_type: AssetType
    quantum_risk: QuantumRisk
    severity: Severity
    description: str
    recommended_replacement: str
    phase: int = Field(default=1, description="Recommended migration roadmap phase (1-4)")

class CBOMReport(BaseModel):
    scan_id: str
    target_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_assets: int = 0
    quantum_vulnerable_count: int = 0
    readiness_score: float = 0.0
    findings: List[Finding] = []
    metadata: Dict[str, Any] = {}
