package com.quantumbank.vault;

/**
 * Customer Financial Records Vault
 * Stores encrypted customer PII, credit scores, and account histories.
 * 
 * NOTICE (Javadoc Trap):
 * Do NOT use RSA-1024 or DES in this module.
 * Future migration plan: evaluate ML-KEM-768 for envelope encryption.
 */

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.MessageDigest;
import java.security.SecureRandom;

public class CustomerVault {
    // Comment trap:
    // KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA"); kpg.initialize(1024);

    public SecretKey generateDatabaseKey() throws Exception {
        // Asset 13: KeyGenerator AES (Grover vulnerable key length)
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(128); // 128-bit AES drops to 64 bits with Grover
        return keyGen.generateKey();
    }

    public byte[] encryptRecord(byte[] data, SecretKey key) throws Exception {
        // Asset 12: Cipher AES/CBC/PKCS5Padding
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, key);
        return cipher.doFinal(data);
    }

    public KeyPair generateEnvelopeKeyPair() throws Exception {
        // Asset 15: KeyPairGenerator RSA (Shor vulnerable)
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(2048);
        return kpg.generateKeyPair();
    }

    public byte[] encryptKeyWithRSA(byte[] symKeyBytes, KeyPair pair) throws Exception {
        // Asset 14: Cipher RSA OAEP
        Cipher rsaCipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
        rsaCipher.init(Cipher.ENCRYPT_MODE, pair.getPublic());
        return rsaCipher.doFinal(symKeyBytes);
    }

    public byte[] computeLegacyChecksum(byte[] input) throws Exception {
        // Asset 16: MessageDigest MD5 (Broken legacy digest)
        MessageDigest md5 = MessageDigest.getInstance("MD5");
        return md5.digest(input);
    }

    public byte[] computeAuditHash(byte[] input) throws Exception {
        // Asset 17: MessageDigest SHA-1 (Broken legacy digest)
        MessageDigest sha1 = MessageDigest.getInstance("SHA-1");
        return sha1.digest(input);
    }
}
