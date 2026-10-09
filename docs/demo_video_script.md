# Q-SHIELD: 3-Minute Video Demo Script
*Track: Enterprise Cybersecurity & Quantum Computing | Q-Hack India 2026*
*Duration: 3:00 Minutes | Human voiceover recording guide*

---

### [0:00 to 0:40] Scene 1: The problem and the Mosca deadline
- On screen: Open on the Q-SHIELD Overview tab. Show the Mosca inequality formula ($X + Y > Z$) and the QuantumBank evaluation.
- Speaker 1:
  > "Welcome. Public-key cryptography protecting enterprise systems has a finite lifespan. When fault-tolerant quantum hardware runs Shor's algorithm, RSA and elliptic-curve schemes fail in polynomial time.
  >
  > The vulnerability begins earlier through harvest now, decrypt later attacks. Attackers capture encrypted financial and healthcare traffic today to decrypt once quantum hardware scales.
  >
  > Under Mosca's inequality, data is exposed when retention requirement X plus migration time Y exceeds time to Q-day Z. In our banking test case, ten years of retention plus 2.3 years of migration equals 12.3 years, which exceeds the estimated 12-year window. We built Q-SHIELD to address this migration gap."

---

### [0:40 to 1:15] Scene 2: Discovery and CycloneDX 1.6 CBOM
- On screen: Switch to the Welcome screen. Click "Run First Scan on QuantumBank". Let the progress bar finish, then open the CBOM Inventory tab.
- Speaker 2:
  > "Q-SHIELD handles the transition from discovery through migration. From our console, we run an automated scan of QuantumBank, a polyglot repository covering Python, Java, Go, JavaScript, and server configurations.
  >
  > The scanner identifies all 27 cryptographic assets with zero false positives from comments or documentation. Every asset is exported to CycloneDX 1.6 Cryptographic Bill of Materials format, highlighting vulnerable RSA, ECDSA, and weakened AES-128 instances."

---

### [1:15 to 1:55] Scene 3: Quantum threat engine and circuit simulation
- On screen: Open the Quantum Simulator tab. Select N = 143 and click "Run Shor Period-Finding". Display the probability peaks and factorization output (11 x 13 = 143). Briefly show the Jupyter notebook (`shor_circuit_simulation.ipynb`) with the Qiskit circuit diagram.
- Speaker 1:
  > "Next, we demonstrate the threat mathematically. In our quantum simulator, we run an exact statevector simulation of Shor's period-finding algorithm on RSA modulus N = 143.
  >
  > The Inverse Quantum Fourier Transform generates constructive interference peaks. By evaluating continued fractions on these peaks, the algorithm extracts period r and factors 143 into 11 and 13.
  >
  > We also include runnable Qiskit quantum circuits in our Jupyter notebook, showing how modular exponentiation collapses classical keys."

---

### [1:55 to 2:35] Scene 4: Active defense and the hybrid PQC gateway
- On screen: Open the PQC Gateway tab. Point out wire sizes (ML-KEM-768: 1,184 B, ML-DSA-65: 3,309 B, Total: 8,954 B). Send a test message. Click "Inject Bit-Flip Ciphertext Tamper" to show the authentication rejection, then click "Simulate Replay Attack" to show the replay drop.
- Speaker 2:
  > "To protect network channels before applications are refactored, Q-SHIELD deploys a hybrid PQC gateway. It combines NIST FIPS 203 ML-KEM-768 key encapsulation with FIPS 204 ML-DSA-65 signatures and classical X25519.
  >
  > The handshake matches the standard FIPS wire footprint at 8,954 bytes. If an attacker flips a single bit in the ciphertext during transit, the AES-256-GCM authentication tag catches the tampering and rejects the packet.
  >
  > If an attacker replays an older recorded packet, sliding-window nonce verification drops it."

---

### [2:35 to 3:00] Scene 5: Phased roadmap and AI copilot
- On screen: Open the Migration Roadmap tab, showing the readiness score increase (33 -> 42 -> 55 -> 84 -> 96). Click "View Diff" on finding FIND-001. Open the AI Copilot tab, click "What should we migrate first?", and point to the export buttons for CycloneDX JSON and the executive report.
- Speaker 1:
  > "Finally, our crypto-agility engine provides a four-phase transition roadmap, raising readiness from 33 to 96 out of 100 with contextual code diffs.
  >
  > The AI copilot verifies every cited finding ID against the database, generating Jira tickets and executive compliance summaries.
  >
  > With 82 automated tests passing and standards-compliant PQC, Q-SHIELD brings verifiable quantum resilience to enterprise systems. Thank you."
