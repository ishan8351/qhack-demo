"""
QuantumBank Core Payment Processing Service
Handles card authorization, batch settlement, and inter-bank clearing.

NOTE FOR DEVELOPERS (Documentation Trap):
Do NOT use RSA-1024 or MD5 in this module. Legacy RSA-2048 will be deprecated by 2030.
Historical references: RSA-512 was factored in 1999.
"""

# Comment trap: We used to support rsa_keygen with 1024 bits
# rsa.generate_private_key(public_exponent=65537, key_size=1024)

import json
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding, dh
from cryptography.hazmat.primitives import hashes

class PaymentProcessor:
    def __init__(self):
        # Asset 1: RSA-2048 key generation (Shor vulnerable)
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def sign_transaction(self, tx_data: bytes) -> bytes:
        """Sign payment transaction payload."""
        # Asset 2: RSA PKCS1v15 signature (Shor vulnerable)
        signature = self.private_key.sign(
            tx_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature

    def verify_transaction(self, tx_data: bytes, signature: bytes) -> bool:
        """Verify merchant transaction signature."""
        try:
            # Asset 3: RSA verification
            self.public_key.verify(
                signature,
                tx_data,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def generate_settlement_dh(self):
        """Establish inter-bank settlement parameters."""
        # Asset 6: Classical Diffie-Hellman parameters (Shor vulnerable)
        parameters = dh.generate_parameters(generator=2, key_size=2048)
        return parameters.generate_private_key()

class BankJWTAuth:
    """Handles JWT generation for banking teller sessions."""

    def issue_teller_token(self, teller_id: str, payment_proc: PaymentProcessor) -> str:
        # Asset 5: JWT RS256 token header
        header = {"alg": "RS256", "typ": "JWT"}
        payload = {"sub": teller_id, "role": "teller", "bank": "QuantumBank"}
        
        encoded_header = base64.urlsafe_b64encode(json.dumps(header).encode()).decode()
        encoded_payload = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
        signing_input = f"{encoded_header}.{encoded_payload}".encode()
        
        # Delegates to PaymentProcessor sign
        sig = payment_proc.sign_transaction(signing_input)
        encoded_sig = base64.urlsafe_b64encode(sig).decode()
        return f"{encoded_header}.{encoded_payload}.{encoded_sig}"

    def decode_teller_token(self, token: str, payment_proc: PaymentProcessor) -> dict:
        # Asset 6: JWT RS256 token verification
        parts = token.split(".")
        header = json.loads(base64.urlsafe_b64decode(parts[0] + "=="))
        if header.get("alg") == "RS256":
            sig = base64.urlsafe_b64decode(parts[2] + "==")
            signing_input = f"{parts[0]}.{parts[1]}".encode()
            if payment_proc.verify_transaction(signing_input, sig):
                return json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
        return {}
