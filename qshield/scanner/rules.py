import re
from typing import List, Dict, Any
from qshield.cbom.schema import AssetType, QuantumRisk, Severity

RULES = [
    # --- Python Cryptography Rules ---
    {
        "id": "PY-RSA-KEYGEN",
        "language": "python",
        "pattern": r"rsa\.generate_private_key\s*\(",
        "algorithm": "RSA-2048 (Keygen)",
        "asset_type": AssetType.KEY,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "Classical RSA keypair generation is completely vulnerable to Shor's algorithm.",
        "recommended_replacement": "ML-DSA-65 (FIPS 204) or Hybrid ML-KEM-768/X25519",
        "phase": 1
    },
    {
        "id": "PY-RSA-SIGN",
        "language": "python",
        "pattern": r"private_key\.sign\s*\(",
        "algorithm": "RSA-2048 (Signature)",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "RSA digital signature algorithm vulnerable to quantum private key derivation.",
        "recommended_replacement": "ML-DSA-65 (FIPS 204)",
        "phase": 1
    },
    {
        "id": "PY-RSA-VERIFY",
        "language": "python",
        "pattern": r"public_key\.verify\s*\(",
        "algorithm": "RSA-2048 (Verification)",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.HIGH,
        "description": "Classical RSA signature verification vulnerable to forged quantum signatures.",
        "recommended_replacement": "ML-DSA-65 (FIPS 204)",
        "phase": 1
    },
    {
        "id": "PY-DH-GEN",
        "language": "python",
        "pattern": r"dh\.generate_parameters\s*\(",
        "algorithm": "Diffie-Hellman-2048",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "Classical finite-field Diffie-Hellman key exchange is broken by Shor's discrete log.",
        "recommended_replacement": "ML-KEM-768 (FIPS 203)",
        "phase": 1
    },
    {
        "id": "PY-JWT-RS256-ISSUE",
        "language": "python",
        "pattern": r'["\']alg["\']\s*:\s*["\']RS256["\']',
        "algorithm": "JWT RS256 (Issue)",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.HIGH,
        "description": "JSON Web Token signed with RSA-2048 (RS256) is vulnerable to token forgery.",
        "recommended_replacement": "JWT with ML-DSA-65 or Ed25519 (Hybrid)",
        "phase": 1
    },
    {
        "id": "PY-JWT-RS256-DECODE",
        "language": "python",
        "pattern": r'header\.get\("alg"\)\s*==\s*"RS256"',
        "algorithm": "JWT RS256 (Verification)",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.HIGH,
        "description": "Token verification trusting RS256 algorithm vulnerable to quantum forgery.",
        "recommended_replacement": "JWT with ML-DSA-65 or Ed25519",
        "phase": 1
    },

    # --- Go Cryptography Rules ---
    {
        "id": "GO-ECDSA-CURVE",
        "language": "go",
        "pattern": r"elliptic\.P256\s*\(\)",
        "algorithm": "ECDSA P-256",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "NIST P-256 elliptic curve discrete logarithm problem is solved by Shor's algorithm.",
        "recommended_replacement": "ML-DSA-65 or SLH-DSA (FIPS 204/205)",
        "phase": 2
    },
    {
        "id": "GO-ECDSA-SIGN",
        "language": "go",
        "pattern": r"ecdsa\.SignASN1\s*\(",
        "algorithm": "ECDSA ASN.1 Sign",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "ECDSA transaction signing is quantum-vulnerable.",
        "recommended_replacement": "ML-DSA-65",
        "phase": 2
    },
    {
        "id": "GO-ECDSA-VERIFY",
        "language": "go",
        "pattern": r"ecdsa\.VerifyASN1\s*\(",
        "algorithm": "ECDSA ASN.1 Verify",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.HIGH,
        "description": "ECDSA transaction verification.",
        "recommended_replacement": "ML-DSA-65",
        "phase": 2
    },
    {
        "id": "GO-SHA256",
        "language": "go",
        "pattern": r"sha256\.Sum256\s*\(",
        "algorithm": "SHA-256",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.SAFE,
        "severity": Severity.LOW,
        "description": "SHA-256 hash function has 128-bit quantum collision resistance (quantum resilient).",
        "recommended_replacement": "Retain SHA-256 or upgrade to SHA-384/SHA-3",
        "phase": 4
    },
    {
        "id": "GO-ECDH-AGREE",
        "language": "go",
        "pattern": r"ecdh\.P256\s*\(\)",
        "algorithm": "ECDH P-256",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "Elliptic Curve Diffie-Hellman key agreement is broken by Shor's algorithm.",
        "recommended_replacement": "Hybrid X25519MLKEM768",
        "phase": 1
    },

    # --- Java Cryptography Rules ---
    {
        "id": "JAVA-AES-GEN",
        "language": "java",
        "pattern": r'KeyGenerator\.getInstance\s*\(\s*"AES"\s*\)',
        "algorithm": "AES-128 (Keygen)",
        "asset_type": AssetType.KEY,
        "quantum_risk": QuantumRisk.WEAKENED,
        "severity": Severity.HIGH,
        "description": "AES-128 key length is degraded to 64-bit security margin under Grover's algorithm.",
        "recommended_replacement": "AES-256-GCM (256-bit key maintains 128-bit quantum strength)",
        "phase": 2
    },
    {
        "id": "JAVA-AES-CIPHER",
        "language": "java",
        "pattern": r'Cipher\.getInstance\s*\(\s*"AES/CBC/PKCS5Padding"\s*\)',
        "algorithm": "AES-128-CBC",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.WEAKENED,
        "severity": Severity.HIGH,
        "description": "AES-128 CBC mode encryption weakened by Grover search and lacking AEAD integrity.",
        "recommended_replacement": "AES-256-GCM (Authenticated Encryption)",
        "phase": 2
    },
    {
        "id": "JAVA-RSA-KEYGEN",
        "language": "java",
        "pattern": r'KeyPairGenerator\.getInstance\s*\(\s*"RSA"\s*\)',
        "algorithm": "RSA-2048 (KeyPairGen)",
        "asset_type": AssetType.KEY,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "Java RSA KeyPairGenerator generates quantum-vulnerable keys.",
        "recommended_replacement": "BouncyCastle PQC ML-KEM / ML-DSA",
        "phase": 3
    },
    {
        "id": "JAVA-RSA-OAEP",
        "language": "java",
        "pattern": r'Cipher\.getInstance\s*\(\s*"RSA/ECB/OAEPWithSHA-256AndMGF1Padding"\s*\)',
        "algorithm": "RSA-OAEP",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "RSA-OAEP envelope encryption broken by Shor's algorithm.",
        "recommended_replacement": "ML-KEM-768 Envelope Encryption",
        "phase": 3
    },
    {
        "id": "JAVA-MD5",
        "language": "java",
        "pattern": r'MessageDigest\.getInstance\s*\(\s*"MD5"\s*\)',
        "algorithm": "MD5",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.DEPRECATED,
        "severity": Severity.HIGH,
        "description": "Classically broken MD5 collision resistance, prohibited by all security standards.",
        "recommended_replacement": "SHA-256 or SHA-3",
        "phase": 2
    },
    {
        "id": "JAVA-SHA1",
        "language": "java",
        "pattern": r'MessageDigest\.getInstance\s*\(\s*"SHA-1"\s*\)',
        "algorithm": "SHA-1",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.DEPRECATED,
        "severity": Severity.MEDIUM,
        "description": "Classically deprecated SHA-1 hash function.",
        "recommended_replacement": "SHA-256 or SHA-384",
        "phase": 2
    },

    # --- JavaScript / WebCrypto Rules ---
    {
        "id": "JS-RSA-OAEP",
        "language": "javascript",
        "pattern": r'name\s*:\s*"RSA-OAEP"',
        "algorithm": "WebCrypto RSA-OAEP",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "Browser WebCrypto RSA-OAEP key exchange broken by quantum computers.",
        "recommended_replacement": "WebCrypto Hybrid or @noble/post-quantum ML-KEM",
        "phase": 1
    },
    {
        "id": "JS-RSA-PKCS1",
        "language": "javascript",
        "pattern": r'name\s*:\s*"RSASSA-PKCS1-v1_5"',
        "algorithm": "WebCrypto RSASSA-PKCS1",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "Client-side RSASSA digital signatures broken by Shor's algorithm.",
        "recommended_replacement": "ML-DSA-65 or Ed25519",
        "phase": 1
    },
    {
        "id": "JS-JWT-RS256",
        "language": "javascript",
        "pattern": r'algorithms\s*:\s*\[\s*"RS256"\s*\]',
        "algorithm": "JWT RS256 Verification",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.HIGH,
        "description": "Client authorization expecting RS256 tokens.",
        "recommended_replacement": "ML-DSA-65 or Hybrid Token Verification",
        "phase": 1
    },
    {
        "id": "JS-SHA256",
        "language": "javascript",
        "pattern": r"(nodeCrypto|crypto)\.createHash\s*\(\s*['\"]sha256['\"]\s*\)",
        "algorithm": "SHA-256",
        "asset_type": AssetType.ALGORITHM,
        "quantum_risk": QuantumRisk.SAFE,
        "severity": Severity.LOW,
        "description": "SHA-256 hashing (Quantum Resilient).",
        "recommended_replacement": "Retain SHA-256",
        "phase": 4
    },

    # --- Configuration Rules (SSH / Nginx) ---
    {
        "id": "CFG-SSH-HOSTKEY",
        "language": "config",
        "pattern": r"HostKeyAlgorithms\s+\+?ssh-rsa",
        "algorithm": "SSH HostKey ssh-rsa",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "SSH host key authentication using legacy RSA is quantum-vulnerable.",
        "recommended_replacement": "OpenSSH sntrup761x25519-sha512 or ML-DSA host keys",
        "phase": 2
    },
    {
        "id": "CFG-SSH-KEX",
        "language": "config",
        "pattern": r"KexAlgorithms\s+.*diffie-hellman",
        "algorithm": "SSH Kex Diffie-Hellman",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.CRITICAL,
        "description": "SSH key exchange using classical DH is vulnerable to passive recording (HNDL).",
        "recommended_replacement": "sntrup761x25519-sha512@openssh.com or mlkem768x25519",
        "phase": 2
    },
    {
        "id": "CFG-TLS-CIPHERS",
        "language": "config",
        "pattern": r"ssl_ciphers\s+['\"].*ECDHE-RSA",
        "algorithm": "TLS ECDHE-RSA CipherSuite",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.BROKEN,
        "severity": Severity.HIGH,
        "description": "Web server TLS cipher suite relies on classical RSA & ECDHE.",
        "recommended_replacement": "TLS 1.3 with Hybrid X25519MLKEM768",
        "phase": 1
    },
    {
        "id": "CFG-TLS-PROTOCOLS",
        "language": "config",
        "pattern": r"ssl_protocols\s+.*TLSv1\.2",
        "algorithm": "TLSv1.2 Protocol",
        "asset_type": AssetType.PROTOCOL,
        "quantum_risk": QuantumRisk.WEAKENED,
        "severity": Severity.MEDIUM,
        "description": "TLS 1.2 lacks native post-quantum cipher negotiations.",
        "recommended_replacement": "Enforce TLS 1.3 only with PQC extensions",
        "phase": 1
    }
]
