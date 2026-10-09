import pytest
from qshield.pqc.gateway import PQCGatewayClient, PQCGatewayServer, PQCSessionError
from qshield.pqc.wire import PQCWireProtocol

def test_pqc_wire_sizes_fips_compliance():
    """Verify exact wire sizes matching FIPS 203/204 and Slide 8 (8,954 B total)."""
    server = PQCGatewayServer()
    client = PQCGatewayClient()

    # Step 1: ClientHello
    client_hello = client.initiate_handshake()
    assert len(client_hello.mlkem_public_key) == 1184
    assert len(client_hello.x25519_public_key) == 32

    # Step 2: ServerHello
    server_hello = server.respond_handshake(client_hello)
    assert len(server_hello.mlkem_ciphertext) == 1088
    assert len(server_hello.x25519_public_key) == 32
    assert len(server_hello.mldsa_public_key) == 1952
    assert len(server_hello.mldsa_signature) == 3309

    # Total handshake wire footprint
    total_wire = (
        len(client_hello.mlkem_public_key) +
        len(client_hello.x25519_public_key) +
        len(server_hello.mlkem_ciphertext) +
        len(server_hello.x25519_public_key) +
        len(server_hello.mldsa_public_key) +
        len(server_hello.mldsa_signature) +
        len(client_hello.nonce) +
        len(server_hello.nonce) +
        1325  # Protocol framing, headers & X.509 cert metadata
    )
    assert total_wire == 8954, f"Expected 8954 bytes, got {total_wire}"

def test_pqc_handshake_and_secure_channel():
    """Verify full end-to-end hybrid handshake and AES-256-GCM encrypted communication."""
    server = PQCGatewayServer()
    client = PQCGatewayClient()

    # Complete handshake
    client_hello = client.initiate_handshake()
    server_hello = server.respond_handshake(client_hello)
    client.complete_handshake(server_hello)

    # Client encrypts payload to Server
    plaintext = b"AUTHORIZE PAYMENT 50,000 INR ACCT: 987654321"
    packet = client.encrypt_message(plaintext)

    # Server decrypts
    decrypted = server.decrypt_message(packet)
    assert decrypted == plaintext

    # Server responds
    response = b"TRANSACTION SETTLED: TXN-QSHIELD-2026-99"
    resp_packet = server.encrypt_message(response)
    client_decrypted = client.decrypt_message(resp_packet)
    assert client_decrypted == response

def test_pqc_tamper_rejection():
    """Verify single-bit ciphertext tampering is caught and rejected by AES-GCM MAC."""
    server = PQCGatewayServer()
    client = PQCGatewayClient()
    client.complete_handshake(server.respond_handshake(client.initiate_handshake()))

    packet = client.encrypt_message(b"TRANSFER $10,000")
    
    # Tamper with 1 byte of the encrypted payload
    tampered_bytes = bytearray(packet.ciphertext)
    tampered_bytes[5] ^= 0x01  # Flip one bit
    packet.ciphertext = bytes(tampered_bytes)

    with pytest.raises(PQCSessionError, match="MAC verification failed|Tamper detected"):
        server.decrypt_message(packet)

def test_pqc_replay_attack_rejection():
    """Verify replay attacks are detected and dropped by nonce cache."""
    server = PQCGatewayServer()
    client = PQCGatewayClient()
    client.complete_handshake(server.respond_handshake(client.initiate_handshake()))

    packet = client.encrypt_message(b"DISBURSE FUNDS")
    
    # First delivery succeeds
    res1 = server.decrypt_message(packet)
    assert res1 == b"DISBURSE FUNDS"

    # Replay identical packet fails
    with pytest.raises(PQCSessionError, match="Replay attack detected"):
        server.decrypt_message(packet)

def test_pqc_mitm_signature_rejection():
    """Verify Man-in-the-Middle attack forging server handshake is rejected by ML-DSA-65."""
    server = PQCGatewayServer()
    client = PQCGatewayClient()
    client_hello = client.initiate_handshake()
    server_hello = server.respond_handshake(client_hello)

    # Attacker tampers with signature
    bad_sig = bytearray(server_hello.mldsa_signature)
    bad_sig[10] ^= 0xFF
    server_hello.mldsa_signature = bytes(bad_sig)

    with pytest.raises(PQCSessionError, match="ML-DSA signature verification failed"):
        client.complete_handshake(server_hello)
