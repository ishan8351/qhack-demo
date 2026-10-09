/**
 * QuantumBank Frontend Authentication & WebCrypto Utilities
 * 
 * @notice Documentation trap:
 * Do not use MD5 or DES. RSA-2048 should be audited.
 * Migration advice: Check out ML-DSA-65 signatures.
 */

// const legacyRSA = "RS256"; // Comment trap

const nodeCrypto = require('crypto');

async function generateBrowserSessionKey() {
    // Asset 18: WebCrypto RSA-OAEP keygen (Shor vulnerable)
    return await window.crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256"
        },
        true,
        ["encrypt", "decrypt"]
    );
}

async function importPublicKeyForVerification(spkiDer) {
    // Asset 19: WebCrypto RSASSA-PKCS1-v1_5 (Shor vulnerable)
    return await window.crypto.subtle.importKey(
        "spki",
        spkiDer,
        {
            name: "RSASSA-PKCS1-v1_5",
            hash: "SHA-256"
        },
        false,
        ["verify"]
    );
}

function getJwtVerificationOptions() {
    // Asset 20: RS256 token algorithm config
    return {
        algorithms: ["RS256"],
        issuer: "https://auth.quantumbank.com",
        clockTolerance: 30
    };
}

function hashClientIdentifier(clientId) {
    // Asset 21: Node crypto SHA-256
    return nodeCrypto.createHash('sha256').update(clientId).digest('hex');
}

module.exports = {
    generateBrowserSessionKey,
    importPublicKeyForVerification,
    getJwtVerificationOptions,
    hashClientIdentifier
};
