package ledger

// QuantumBank Blockchain & Ledger Settlement Service
// NOTE: Comment trap: We must never allow RSA-1024 or MD5 in production ledgers.
// // Deprecated: crypto/rsa will be removed in v3.

import (
	"crypto/ecdh"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/sha256"
)

type Block struct {
	Index        int64
	Timestamp    int64
	PrevHash     [32]byte
	Transactions [][]byte
	Hash         [32]byte
}

type LedgerService struct {
	curve elliptic.Curve
}

func NewLedgerService() *LedgerService {
	// Asset 7: ECDSA P-256 curve selection (Shor vulnerable)
	return &LedgerService{
		curve: elliptic.P256(),
	}
}

func (s *LedgerService) GenerateLedgerKey() (*ecdsa.PrivateKey, error) {
	// ECDSA Key generation using P-256
	return ecdsa.GenerateKey(s.curve, rand.Reader)
}

func (s *LedgerService) SignBlock(priv *ecdsa.PrivateKey, blockData []byte) ([]byte, error) {
	// Asset 10: SHA-256 hashing
	hash := sha256.Sum256(blockData)
	
	// Asset 8: ECDSA ASN.1 signature (Shor vulnerable)
	return ecdsa.SignASN1(rand.Reader, priv, hash[:])
}

func (s *LedgerService) VerifyBlock(pub *ecdsa.PublicKey, hash [32]byte, sig []byte) bool {
	// Asset 9: ECDSA ASN.1 signature verification
	return ecdsa.VerifyASN1(pub, hash[:], sig)
}

func (s *LedgerService) PerformPeerECDH(peerPublicKeyBytes []byte) ([]byte, error) {
	// Asset 11: ECDH P-256 key agreement (Shor vulnerable)
	curve := ecdh.P256()
	privKey, err := curve.GenerateKey(rand.Reader)
	if err != nil {
		return nil, err
	}
	pubKey, err := curve.NewPublicKey(peerPublicKeyBytes)
	if err != nil {
		return nil, err
	}
	return privKey.ECDH(pubKey)
}
