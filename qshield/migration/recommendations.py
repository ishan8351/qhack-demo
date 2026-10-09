from typing import Optional
from qshield.cbom.schema import Finding

def get_code_replacement_diff(finding: Finding) -> str:
    """
    Generates a unified diff suggestion replacing the vulnerable cryptographic
    construct with post-quantum standards (NIST FIPS 203/204 or AES-256).
    """
    alg = finding.algorithm.upper()
    snippet = finding.code_snippet

    # Python RSA Keygen
    if "RSA" in alg and ("KEYGEN" in alg or "generate_private_key" in snippet):
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (Post-Quantum Hybrid)\n"
            f"- from cryptography.hazmat.primitives.asymmetric import rsa\n"
            f"+ from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa\n"
            f"- self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)\n"
            f"+ self.private_key = mlkem.MLKEM768PrivateKey.generate() # FIPS 203 Post-Quantum\n"
        )

    # Python RSA Signature / Verification
    elif "RSA" in alg and ("SIGN" in alg or "sign" in snippet):
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (ML-DSA-65 Signature)\n"
            f"- signature = self.private_key.sign(tx_data, padding.PKCS1v15(), hashes.SHA256())\n"
            f"+ # Migrate to ML-DSA-65 (FIPS 204 Digital Signature Algorithm)\n"
            f"+ signature = self.mldsa_private_key.sign(tx_data)\n"
        )

    elif "RSA" in alg and ("VERIFY" in alg or "verify" in snippet):
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (ML-DSA-65 Verification)\n"
            f"- self.public_key.verify(signature, tx_data, padding.PKCS1v15(), hashes.SHA256())\n"
            f"+ self.mldsa_public_key.verify(signature, tx_data)\n"
        )

    # Diffie-Hellman / ECDH
    elif "DIFFIE-HELLMAN" in alg or "ECDH" in alg:
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (Hybrid ML-KEM-768/X25519)\n"
            f"- parameters = dh.generate_parameters(generator=2, key_size=2048)\n"
            f"+ # Migrate to Post-Quantum Hybrid KEM (FIPS 203)\n"
            f"+ kem_priv = mlkem.MLKEM768PrivateKey.generate()\n"
        )

    # JWT RS256
    elif "RS256" in alg or "JWT" in alg:
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (Post-Quantum Token)\n"
            f'- header = {{"alg": "RS256", "typ": "JWT"}}\n'
            f'+ # Migrate from RS256 to ML-DSA-65 or Ed25519\n'
            f'+ header = {{"alg": "ML-DSA-65", "typ": "JWT"}}\n'
        )

    # Java AES-128
    elif "AES-128" in alg or ("AES" in alg and "128" in alg):
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (AES-256-GCM AEAD)\n"
            f"- KeyGenerator keyGen = KeyGenerator.getInstance(\"AES\"); keyGen.init(128);\n"
            f"+ KeyGenerator keyGen = KeyGenerator.getInstance(\"AES\"); keyGen.init(256); // 128-bit Grover Resilient\n"
            f"- Cipher cipher = Cipher.getInstance(\"AES/CBC/PKCS5Padding\");\n"
            f"+ Cipher cipher = Cipher.getInstance(\"AES/GCM/NoPadding\");\n"
        )

    # Java RSA OAEP
    elif "RSA-OAEP" in alg:
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (BouncyCastle ML-KEM-768)\n"
            f"- Cipher.getInstance(\"RSA/ECB/OAEPWithSHA-256AndMGF1Padding\");\n"
            f"+ // Migrate to BouncyCastle FIPS ML-KEM-768 Key Encapsulation\n"
            f"+ MLKEMKeyPairGenerator kpg = new MLKEMKeyPairGenerator();\n"
        )

    # SSH Config
    elif "SSH" in alg and "HOSTKEY" in alg:
        return (
            f"--- {finding.file_path} (Line {finding.line_number})\n"
            f"+++ {finding.file_path} (OpenSSH Post-Quantum HostKeys)\n"
            f"- HostKeyAlgorithms +ssh-rsa,rsa-sha2-512\n"
            f"+ HostKeyAlgorithms ssh-ed25519,sntrup761x25519-sha512@openssh.com\n"
        )

    # Default generic diff
    return (
        f"--- {finding.file_path} (Line {finding.line_number})\n"
        f"+++ {finding.file_path} (Post-Quantum Migration)\n"
        f"- {finding.code_snippet}\n"
        f"+ // Recommended: {finding.recommended_replacement}\n"
    )
