from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa, x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class PQCPrimitives:
    """
    Hardware-accelerated NIST Post-Quantum Cryptography Primitives
    FIPS 203 (ML-KEM-768), FIPS 204 (ML-DSA-65), and classical X25519 / AES-256-GCM.
    """

    @staticmethod
    def generate_mlkem_keypair():
        priv = mlkem.MLKEM768PrivateKey.generate()
        return priv, priv.public_key()

    @staticmethod
    def generate_mldsa_keypair():
        priv = mldsa.MLDSA65PrivateKey.generate()
        return priv, priv.public_key()

    @staticmethod
    def generate_x25519_keypair():
        priv = x25519.X25519PrivateKey.generate()
        return priv, priv.public_key()

    @staticmethod
    def derive_hybrid_session_key(kem_secret: bytes, ecdh_secret: bytes, salt: bytes = b"Q-SHIELD-HYBRID-SALT") -> bytes:
        """
        Derives an AES-256-GCM key by combining post-quantum and classical shared secrets via HKDF-SHA256.
        """
        combined = kem_secret + ecdh_secret
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            info=b"Q-SHIELD-V1-AES-256-GCM"
        )
        return hkdf.derive(combined)
