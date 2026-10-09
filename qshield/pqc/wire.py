import time
import os
from typing import NamedTuple
from pydantic import BaseModel, Field

class ClientHello(BaseModel):
    mlkem_public_key: bytes
    x25519_public_key: bytes
    nonce: bytes = Field(default_factory=lambda: os.urandom(16))
    timestamp: float = Field(default_factory=time.time)

class ServerHello(BaseModel):
    mlkem_ciphertext: bytes
    x25519_public_key: bytes
    mldsa_public_key: bytes
    mldsa_signature: bytes
    nonce: bytes = Field(default_factory=lambda: os.urandom(16))
    timestamp: float = Field(default_factory=time.time)

class EncryptedPacket(BaseModel):
    nonce: bytes
    ciphertext: bytes
    tag: bytes
    sequence_number: int

class PQCWireProtocol:
    HEADER_MAGIC = b"QSHIELD"
    VERSION = 1
