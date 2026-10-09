import os
import pytest
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature
from qshield.pqc.primitives import PQCPrimitives
from qshield.pqc.gateway import PQCGatewayClient, PQCGatewayServer, PQCSessionError

def test_mlkem_keygen_properties():
    priv, pub = PQCPrimitives.generate_mlkem_keypair()
    assert len(pub.public_bytes_raw()) == 1184

def test_mlkem_encap_decap_correctness():
    priv, pub = PQCPrimitives.generate_mlkem_keypair()
    secret_sender, ct = pub.encapsulate()
    secret_receiver = priv.decapsulate(ct)
    assert secret_sender == secret_receiver
    assert len(secret_sender) == 32
    assert len(ct) == 1088

def test_mlkem_mismatch_ciphertext_fails():
    priv, pub = PQCPrimitives.generate_mlkem_keypair()
    secret_sender, ct = pub.encapsulate()
    bad_ct = bytearray(ct)
    bad_ct[10] ^= 0x01
    # FIPS 203 uses Fujisaki-Okamoto transform: invalid ciphertext yields mismatched pseudorandom secret
    secret_mismatch = priv.decapsulate(bytes(bad_ct))
    assert secret_mismatch != secret_sender

def test_mldsa_keygen_properties():
    priv, pub = PQCPrimitives.generate_mldsa_keypair()
    assert len(pub.public_bytes_raw()) == 1952

def test_mldsa_sign_verify_correctness():
    priv, pub = PQCPrimitives.generate_mldsa_keypair()
    msg = b"Financial Clearance Payload 2026"
    sig = priv.sign(msg)
    assert len(sig) == 3309
    pub.verify(sig, msg)

def test_mldsa_tampered_message_fails():
    priv, pub = PQCPrimitives.generate_mldsa_keypair()
    msg = b"VALID TRANSACTION"
    sig = priv.sign(msg)
    with pytest.raises(InvalidSignature):
        pub.verify(sig, b"FORGED TRANSACTION")

def test_mldsa_tampered_signature_fails():
    priv, pub = PQCPrimitives.generate_mldsa_keypair()
    msg = b"VALID TRANSACTION"
    sig = bytearray(priv.sign(msg))
    sig[20] ^= 0xAA
    with pytest.raises(InvalidSignature):
        pub.verify(bytes(sig), msg)

def test_x25519_diffie_hellman_match():
    p1, pub1 = PQCPrimitives.generate_x25519_keypair()
    p2, pub2 = PQCPrimitives.generate_x25519_keypair()
    s1 = p1.exchange(pub2)
    s2 = p2.exchange(pub1)
    assert s1 == s2
    assert len(s1) == 32

def test_hybrid_kdf_entropy_combination():
    kem_s = os.urandom(32)
    ecdh_s = os.urandom(32)
    key1 = PQCPrimitives.derive_hybrid_session_key(kem_s, ecdh_s)
    key2 = PQCPrimitives.derive_hybrid_session_key(kem_s, ecdh_s)
    assert key1 == key2
    assert len(key1) == 32

def test_aes_gcm_empty_string():
    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, b"", None)
    pt = aes.decrypt(nonce, ct, None)
    assert pt == b""

def test_aes_gcm_large_payload():
    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    payload = b"A" * 1_000_000
    ct = aes.encrypt(nonce, payload, None)
    pt = aes.decrypt(nonce, ct, None)
    assert pt == payload

def test_aes_gcm_wrong_tag_raises():
    key = AESGCM.generate_key(bit_length=256)
    aes = AESGCM(key)
    nonce = os.urandom(12)
    ct = bytearray(aes.encrypt(nonce, b"Secret Data", None))
    ct[-1] ^= 0x01
    with pytest.raises(Exception):
        aes.decrypt(nonce, bytes(ct), None)

def test_server_nonce_uniqueness():
    server = PQCGatewayServer()
    nonces = set()
    for _ in range(20):
        client = PQCGatewayClient()
        hello = client.initiate_handshake()
        resp = server.respond_handshake(hello)
        assert resp.nonce not in nonces
        nonces.add(resp.nonce)

def test_client_nonce_uniqueness():
    client = PQCGatewayClient()
    nonces = set()
    for _ in range(20):
        hello = client.initiate_handshake()
        assert hello.nonce not in nonces
        nonces.add(hello.nonce)
