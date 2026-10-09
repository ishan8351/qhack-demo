import os
import time
from typing import Set, Optional
from cryptography.hazmat.primitives.asymmetric import mlkem, mldsa, x25519
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from qshield.pqc.wire import ClientHello, ServerHello, EncryptedPacket
from qshield.pqc.primitives import PQCPrimitives

class PQCSessionError(Exception):
    """Raised when cryptographic verification, tampering, or replay attack is detected."""
    pass

class PQCGatewayServer:
    def __init__(self):
        # Server long-term identity authentication key (ML-DSA-65)
        self.dsa_priv, self.dsa_pub = PQCPrimitives.generate_mldsa_keypair()
        self.seen_nonces: Set[bytes] = set()
        self.session_key: Optional[bytes] = None
        self.aesgcm: Optional[AESGCM] = None
        self.seq_num = 0

    def respond_handshake(self, client_hello: ClientHello) -> ServerHello:
        # Replay prevention for handshake nonces
        if client_hello.nonce in self.seen_nonces:
            raise PQCSessionError("Replay attack detected on ClientHello nonce")
        self.seen_nonces.add(client_hello.nonce)

        # 1. Reconstruct client ML-KEM public key
        client_kem_pub = mlkem.MLKEM768PublicKey.from_public_bytes(client_hello.mlkem_public_key)
        
        # 2. Encapsulate shared secret using ML-KEM-768
        kem_shared_secret, kem_ciphertext = client_kem_pub.encapsulate()

        # 3. Generate server ephemeral X25519 keypair and perform ECDH
        server_x25519_priv, server_x25519_pub = PQCPrimitives.generate_x25519_keypair()
        client_x25519_pub = x25519.X25519PublicKey.from_public_bytes(client_hello.x25519_public_key)
        ecdh_shared_secret = server_x25519_priv.exchange(client_x25519_pub)

        # 4. Derive AES-256-GCM session key
        self.session_key = PQCPrimitives.derive_hybrid_session_key(kem_shared_secret, ecdh_shared_secret)
        self.aesgcm = AESGCM(self.session_key)

        # 5. Sign ServerHello transcript using ML-DSA-65
        server_nonce = os.urandom(16)
        server_pub_bytes = server_x25519_pub.public_bytes_raw()
        transcript = kem_ciphertext + server_pub_bytes + server_nonce + client_hello.nonce
        mldsa_sig = self.dsa_priv.sign(transcript)

        return ServerHello(
            mlkem_ciphertext=kem_ciphertext,
            x25519_public_key=server_pub_bytes,
            mldsa_public_key=self.dsa_pub.public_bytes_raw(),
            mldsa_signature=mldsa_sig,
            nonce=server_nonce,
            timestamp=time.time()
        )

    def decrypt_message(self, packet: EncryptedPacket) -> bytes:
        if not self.aesgcm:
            raise PQCSessionError("No active cryptographic session")

        # Replay prevention on packet nonces
        if packet.nonce in self.seen_nonces:
            raise PQCSessionError("Replay attack detected: packet nonce already consumed")
        self.seen_nonces.add(packet.nonce)

        try:
            # AES-GCM expects ciphertext + 16-byte tag
            combined_ct = packet.ciphertext + packet.tag
            plaintext = self.aesgcm.decrypt(packet.nonce, combined_ct, str(packet.sequence_number).encode())
            return plaintext
        except Exception as e:
            raise PQCSessionError(f"MAC verification failed: Tamper detected ({str(e)})")

    def encrypt_message(self, plaintext: bytes) -> EncryptedPacket:
        if not self.aesgcm:
            raise PQCSessionError("No active cryptographic session")
        nonce = os.urandom(12)
        self.seq_num += 1
        combined_ct = self.aesgcm.encrypt(nonce, plaintext, str(self.seq_num).encode())
        # Split 16-byte GCM tag
        ct = combined_ct[:-16]
        tag = combined_ct[-16:]
        return EncryptedPacket(
            nonce=nonce,
            ciphertext=ct,
            tag=tag,
            sequence_number=self.seq_num
        )


class PQCGatewayClient:
    def __init__(self):
        self.kem_priv: Optional[mlkem.MLKEM768PrivateKey] = None
        self.kem_pub: Optional[mlkem.MLKEM768PublicKey] = None
        self.x25519_priv: Optional[x25519.X25519PrivateKey] = None
        self.x25519_pub: Optional[x25519.X25519PublicKey] = None
        self.client_nonce: Optional[bytes] = None
        self.session_key: Optional[bytes] = None
        self.aesgcm: Optional[AESGCM] = None
        self.seq_num = 0
        self.seen_nonces: Set[bytes] = set()

    def initiate_handshake(self) -> ClientHello:
        self.kem_priv, self.kem_pub = PQCPrimitives.generate_mlkem_keypair()
        self.x25519_priv, self.x25519_pub = PQCPrimitives.generate_x25519_keypair()
        self.client_nonce = os.urandom(16)

        return ClientHello(
            mlkem_public_key=self.kem_pub.public_bytes_raw(),
            x25519_public_key=self.x25519_pub.public_bytes_raw(),
            nonce=self.client_nonce,
            timestamp=time.time()
        )

    def complete_handshake(self, server_hello: ServerHello):
        # 1. Verify ML-DSA-65 signature on ServerHello transcript
        server_dsa_pub = mldsa.MLDSA65PublicKey.from_public_bytes(server_hello.mldsa_public_key)
        transcript = server_hello.mlkem_ciphertext + server_hello.x25519_public_key + server_hello.nonce + self.client_nonce
        try:
            server_dsa_pub.verify(server_hello.mldsa_signature, transcript)
        except Exception as e:
            raise PQCSessionError(f"ML-DSA signature verification failed: {str(e)}")

        # 2. Decapsulate ML-KEM shared secret
        kem_shared_secret = self.kem_priv.decapsulate(server_hello.mlkem_ciphertext)

        # 3. Perform ECDH with server's X25519 public key
        server_x25519_pub = x25519.X25519PublicKey.from_public_bytes(server_hello.x25519_public_key)
        ecdh_shared_secret = self.x25519_priv.exchange(server_x25519_pub)

        # 4. Derive AES-256-GCM session key
        self.session_key = PQCPrimitives.derive_hybrid_session_key(kem_shared_secret, ecdh_shared_secret)
        self.aesgcm = AESGCM(self.session_key)

    def encrypt_message(self, plaintext: bytes) -> EncryptedPacket:
        if not self.aesgcm:
            raise PQCSessionError("No active cryptographic session")
        nonce = os.urandom(12)
        self.seq_num += 1
        combined_ct = self.aesgcm.encrypt(nonce, plaintext, str(self.seq_num).encode())
        ct = combined_ct[:-16]
        tag = combined_ct[-16:]
        return EncryptedPacket(
            nonce=nonce,
            ciphertext=ct,
            tag=tag,
            sequence_number=self.seq_num
        )

    def decrypt_message(self, packet: EncryptedPacket) -> bytes:
        if not self.aesgcm:
            raise PQCSessionError("No active cryptographic session")
        if packet.nonce in self.seen_nonces:
            raise PQCSessionError("Replay attack detected: packet nonce already consumed")
        self.seen_nonces.add(packet.nonce)

        try:
            combined_ct = packet.ciphertext + packet.tag
            return self.aesgcm.decrypt(packet.nonce, combined_ct, str(packet.sequence_number).encode())
        except Exception as e:
            raise PQCSessionError(f"MAC verification failed: Tamper detected ({str(e)})")
