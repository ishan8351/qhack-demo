# Q-SHIELD: 10-Slide Hackathon Presentation Deck Blueprint
*Adhering to the official template structure in Q-SHIELD.pptx.pdf and hackathon guidelines (10 slides maximum).*

---

## Slide 1: Title and overview

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Team Name: [Your Team Name]                Track: Enterprise Cybersecurity & |
|  Team Lead Name: [Lead Name]                       Quantum Computing          |
|  Problem Statement: Post-Quantum Cryptography Migration & Asset Discovery     |
|                                                                               |
|                                  Q-SHIELD                                     |
|                   End-to-End Quantum Security Platform                        |
|                                                                               |
|       Discover, understand, protect and migrate quantum-vulnerable            |
|                           cryptography before Q-day                           |
|                                                                               |
|                               Q-Hack India 2026                               |
+-------------------------------------------------------------------------------+
```

### Slide content
Track: Enterprise Cybersecurity & Quantum Computing
Problem statement: Post-Quantum Cryptography Discovery, Simulation, and Agile Migration
Title: Q-SHIELD: End-to-End Quantum Security Platform
Subtitle: Discover, understand, protect, and migrate quantum-vulnerable cryptography before Q-day
Event: Q-Hack India 2026
Tagline: The complete lifecycle from Cryptographic Bill of Materials (CBOM) to active hybrid PQC defense.

---

## Slide 2: Problem: Today's public-key cryptography has an expiry date

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Problem: Today's public-key cryptography has an expiry date                  |
+-----------------------+-----------------------+-------------------------------+
|  [ 1 ]                |  [ 2 ]                |  [ 3 ]                        |
|  Shor breaks RSA & ECC|  Harvest now, decrypt |  No inventory, no plan        |
|                       |  later (HNDL)         |                               |
|  A large fault-       |  Attackers record     |  Most organizations cannot    |
|  tolerant quantum     |  encrypted traffic    |  say where vulnerable         |
|  computer running     |  and stolen data      |  cryptography lives in their  |
|  Shor's algorithm     |  today, then decrypt  |  code, configs and certs, so  |
|  derives private keys |  it once quantum      |  they cannot prioritize a     |
|  from public keys.    |  computers mature.    |  migration that takes years.  |
|  RSA, ECDSA, ECDH     |  Long-lived data is   |                               |
|  and DH all fall.     |  exposed already.     |                               |
+-----------------------+-----------------------+-------------------------------+
|  The clock is set: NIST standardized ML-KEM, ML-DSA and SLH-DSA in Aug 2024    |
|  (FIPS 203-205) and plans to deprecate quantum-vulnerable public-key           |
|  algorithms after 2030 (NIST IR 8547, draft).                                 |
+-------------------------------------------------------------------------------+
```

### Slide content
Title: Problem: Today's public-key cryptography has an expiry date

Column 1: Shor breaks RSA and ECC
- A fault-tolerant quantum computer running Shor's algorithm derives private keys from public keys in polynomial time.
- RSA, ECDSA, ECDH, and Diffie-Hellman fail entirely.

Column 2: Harvest now, decrypt later (HNDL)
- Attackers record encrypted network traffic and exfiltrate ciphertext today to decrypt once quantum hardware scales.
- Long-lived financial, healthcare, and state data is already exposed.

Column 3: Missing inventory and migration plans
- Most organizations lack visibility into where vulnerable algorithms live across polyglot repositories, configurations, and certificates.
- Without an inventory, security teams cannot sequence a migration that takes years.

Regulatory timeline:
- NIST finalized ML-KEM, ML-DSA, and SLH-DSA in August 2024 (FIPS 203-205) and plans to deprecate quantum-vulnerable public-key algorithms after 2030 (NIST IR 8547).

---

## Slide 3: Why it matters: The deadline is set by your data, not by quantum computers

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Why It Matters: The deadline is set by your data, not by quantum computers   |
+---------------------------------------+---------------------------------------+
|  Who faces it:                        |  Mosca's inequality: data is at risk  |
|                                       |  when:        X  +  Y  >  Z           |
|  1. Banks & payments                  |                                       |
|     transaction records, card data,   |  X = years data must stay secret      |
|     inter-bank keys                   |  Y = years to migrate                 |
|  2. Healthcare                        |  Z = years until Q-day                |
|     medical records kept for decades  +---------------------------------------+
|  3. Government & defense              |  Example from our scan:               |
|     classified and citizen data       |  QuantumBank payment-api              |
|  4. Any organization                  |  • records kept: 10 y (X)             |
|     with data that must stay secret   |  • migrate: 2.3 y (Y)                 |
|     10+ years                         |  • Q-day ≈ 12 y (Z)                   |
|                                       |  Result: 10 + 2.3 = 12.3 > 12.0 y     |
|                                       |  RSA-protected financial records      |
|                                       |  outlive encryption -> High exposure. |
+---------------------------------------+---------------------------------------+
```

### Slide content
Title: Why it matters: The deadline is set by your data, not by quantum computers

Target sectors:
1. Banks and payments: Transaction archives, credit card data, and inter-bank clearing keys with 10+ year retention mandates.
2. Healthcare: Patient medical histories and genomic data preserved for decades.
3. Government and defense: Classified intelligence, national identity registries, and citizen records.
4. Enterprise: Contracts, intellectual property, and core financial records.

Mosca's mathematical inequality:
- Data is compromised when: $X + Y > Z$
- $X$ = years data must stay secret
- $Y$ = years required to complete migration
- $Z$ = years until a cryptanalytically relevant quantum computer arrives

Scan evaluation on QuantumBank `payment-api`:
- Retention obligation: 10.0 years ($X$)
- Migration window: 2.3 years ($Y$)
- Estimated time to Q-day: 12.0 years ($Z$)
- Total risk window: $10.0 + 2.3 = 12.3\text{ years} > 12.0\text{ years}$ ($Z$)
- Result: RSA-protected financial records outlive their cryptographic lifespan today.

---

## Slide 4: Proposed solution: One platform from discovery to migration

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Proposed Solution: One platform from discovery to migration                  |
+-------------------+-------------------+-------------------+-------------------+
|  [ 1 ] DISCOVER   |  [ 2 ] UNDERSTAND |  [ 3 ] PROTECT    |  [ 4 ] MIGRATE    |
|  Crypto scanner   |  Risk & threat    |  PQC gateway      |  Crypto-agility   |
|                   |                   |                   |                   |
|  Scans Python,    |  Readiness score  |  Quantum-safe     |  A replacement for|
|  Java, JS and Go  |  0-100, HNDL      |  channel with     |  every finding,   |
|  code, SSH/JWT    |  exposure per     |  ML-KEM-768 key   |  a 4-phase        |
|  configs, X.509   |  data class, Shor |  exchange and     |  roadmap and      |
|  certs and keys   |  and Grover       |  ML-DSA-65 sigs,  |  projected        |
|  into a CBOM.     |  simulated.       |  hybrid X25519.   |  readiness score. |
+-------------------+-------------------+-------------------+-------------------+
|  [ 5 ] AI SECURITY COPILOT: Explains the risk, answers "what first?", writes   |
|  developer tickets and an executive report, grounded only in the scan.       |
+-------------------------------------------------------------------------------+
```

### Slide content
Title: Proposed solution: One platform from discovery to migration

The four pillars:
1. Discover (Crypto scanner): Scans Python, Java, JavaScript, and Go code, SSH and JWT configurations, X.509 certificates, and committed keys into a CycloneDX 1.6 Cryptographic Bill of Materials (CBOM).
2. Understand (Risk and quantum threat): Evaluates readiness scores (0 to 100), HNDL exposure per data class, and exact mathematical simulations of Shor's and Grover's algorithms.
3. Protect (PQC gateway): Drop-in quantum-safe proxy with ML-KEM-768 key encapsulation and ML-DSA-65 signatures, hybridized with X25519.
4. Migrate (Crypto-agility engine): Supplies code replacements for each finding, a 4-phase transition roadmap, and projected readiness scores across milestones.

AI Security Copilot:
Explains vulnerability posture, answers remediation questions, generates developer tickets, and produces executive compliance reports, strictly grounded in the CBOM database.

---

## Slide 5: Why quantum? Quantum computing is both the threat and our method

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Why Quantum? Quantum computing is both the threat and our method            |
+---------------------------------------+---------------------------------------+
|  THE THREAT                           |  OUR METHOD                           |
|                                       |                                       |
|  • Shor's algorithm: [ BROKEN ]       |  • Exact statevector simulation of    |
|    Exponential speedup for factoring   |    Shor's period finding: modular     |
|    and discrete logarithms: RSA and   |    exponentiation, inverse QFT,       |
|    elliptic-curve keys derived from   |    measurement, then continued        |
|    public keys.                       |    fractions and gcd.                 |
|                                       |  • Post-quantum ML-KEM / ML-DSA are   |
|  • Grover's algorithm: [ WEAKENED ]   |    engineered to resist this adversary|
|    Quadratic speedup for brute-force: |                                       |
|    AES-128 drops to 64-bit strength;  |                                       |
|    AES-256 retains 128-bit strength.  |                                       |
+---------------------------------------+---------------------------------------+
|  SHOR SIMULATION, N = 15, a = 7: Peaks occur every Q/r = 64                   |
|                                                                               |
|   Probability                                                                 |
|   0.25 |      ||               ||               ||               ||           |
|   0.20 |      ||               ||               ||               ||           |
|   0.10 |      ||               ||               ||               ||           |
|      0 +------+----------------+----------------+----------------+----> State |
|        0      64              128              192              256           |
+-------------------------------------------------------------------------------+
```

### Slide content
Title: Why quantum? Quantum computing is both the threat and our method

The threat:
- Shor's algorithm (broken): Exponential speedup for integer factorization and discrete logarithms. Derives private keys from public keys in polynomial time.
- Grover's algorithm (weakened): Quadratic speedup for symmetric key searches. AES-128 drops to 64-bit effective security; AES-256 retains 128-bit security.

Our method:
- Exact statevector simulation of Shor's period finding: Superposition registers, modular exponentiation $f(x) = a^x \bmod N$, inverse QFT constructive interference, measurement, continued fractions, and gcd.
- Verifies that lattice-based schemes (ML-KEM and ML-DSA) lack the periodic abelian structure that Shor's algorithm exploits.

Simulation verification ($N = 15, a = 7$):
- Superposition over $Q = 2^8 = 256$ states with period $r = 4$.
- Constructive interference produces measurement peaks at intervals of $Q/r = 64$ ($s \in \{0, 64, 128, 192\}$).

---

## Slide 6: Implementation and architecture: One inventory feeds every module

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Implementation and Architecture: One inventory feeds every module            |
+-------------------+-----------------------------------+-----------------------+
|  INPUTS           |  FASTAPI BACKEND (PYTHON)         |  OUTPUTS              |
|                   |                                   |                       |
|  • Git repository |  +-----------------------------+  |  • Dashboard (7 tabs) |
|  • ZIP upload     |  | Crypto scanner              |  |  • Quantum-safe chat  |
|  • Source code    |  | Risk engine                 |  |  • Executive report   |
|  • Configs        |  | Migration engine            |  |  • Developer tickets  |
|  • Certificates   |  | HNDL analyzer               |  |  • CBOM export        |
|    & keys         |  | PQC gateway                 |  |    (CycloneDX 1.6)    |
|                   |  | Quantum simulator           |  |                       |
|                   |  | AI copilot                  |  |                       |
|                   |  +-----------------------------+  |                       |
|                   |   CBOM (JSON schema) • SQLite     |                       |
+-------------------+-----------------------------------+-----------------------+
|  LEGEND: ■ quantum simulation   ■ post-quantum cryptography   □ classical     |
|                                                                               |
|  TECH STACK: Python • FastAPI • pyca/cryptography (OpenSSL) for ML-KEM-768,   |
|  ML-DSA-65, AES-256-GCM • NumPy statevector • Claude/Gemini API • SQLite •    |
|  Plain JS + SVG • Docker / Podman                                             |
+-------------------------------------------------------------------------------+
```

### Slide content
Title: Implementation and architecture: One inventory feeds every module

Inputs:
- Git repository URLs, uploaded ZIP archives, source code files, server configurations, X.509 certificates and private keys.

FastAPI backend:
- Crypto scanner: Polyglot static analyzer with comment and docstring stripping.
- Risk and HNDL engine: Quantifies Mosca risk and calculates 0 to 100 readiness scores.
- Quantum simulator: Statevector Shor and Grover engines in NumPy.
- PQC gateway: Hybrid ML-KEM-768 and X25519 channel with ML-DSA-65 signatures.
- Migration engine: Contextual code diff generator across four transition phases.
- AI copilot: Grounded security advisor backed by local CBOM SQLite storage.

Outputs:
- Seven-tab web dashboard, live quantum-safe chat, executive audit reports, Jira and GitHub remediation tickets, and CycloneDX 1.6 CBOM JSON.

Technology stack:
- Python, FastAPI, pyca/cryptography (OpenSSL 3.5), NumPy, SQLite, plain JavaScript and SVG, Docker.

---

## Slide 7: Working prototype: Verification and live controls

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Working Prototype: Verification and live controls                            |
+-----------------------+-----------------------+-------------------------------+
|  [ TILE 1 ]           |  [ TILE 2 ]           |  [ TILE 3 ]                   |
|  Shor Simulation on   |  ML-KEM Chat, Tamper  |  Roadmap:                     |
|  143                  |  Rejected             |  33 -> 84 -> 96               |
|                       |                       |                               |
|  Exact statevector    |  Hybrid handshake +   |  4-phase migration            |
|  period finding       |  AES-256-GCM session; |  planner recalculating        |
|  factors 143 into     |  bit-flip tamper      |  readiness score at each      |
|  11 x 13 in <0.2s.    |  triggers instant MAC |  stage of deployment.         |
|                       |  failure.             |                               |
+-----------------------+-----------------------+-------------------------------+
|  [ TILE 4 ]                                   |  [ TILE 5 ]                   |
|  Grounded AI Copilot                          |  Overview: Scan of QuantumBank|
|                                               |                               |
|  Explains risks, generates tickets & reports; |  Discovers 27 assets across 4 |
|  strictly validates finding IDs against CBOM  |  languages; initial readiness |
|  to eliminate hallucinations.                 |  score evaluated at 33/100.   |
+-----------------------------------------------+-------------------------------+
```

### Slide content
Title: Working prototype: Verification and live controls

System capabilities demonstrated:
1. Shor simulation on N = 143: Exact statevector period finding factors 143 into 11 x 13, displaying IQFT probability amplitudes and continued fraction convergents.
2. ML-KEM chat and tamper rejection: Interactive hybrid channel. Flipping a single bit in the ciphertext triggers an AEAD tag mismatch and drops the message.
3. Phased roadmap (33 -> 42 -> 55 -> 84 -> 96): Dynamic readiness modeling across four structured phases with unified code diffs.
4. Grounded AI copilot: Creates remediation tickets and compliance summaries while verifying finding IDs against the database to prevent hallucinations.
5. Overview console: Live scan of QuantumBank identifying 27 cryptographic assets, computing 33/100 baseline readiness and highlighting HNDL risk.

---

## Slide 8: Results and validation: Validated on a seeded bank end to end

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Results / Validation: Validated on a seeded bank, end to end                 |
+-------------------+-------------------+-------------------+-------------------+
|     27 / 27       |     33 -> 84      |    8,954 BYTES    |        84         |
|  seeded crypto    |  readiness score  |  hybrid ML-KEM-   |  automated tests  |
|  assets found in  |  after roadmap    |  768 + ML-DSA-65  |  passing, tamper, |
|  QuantumBank, 0   |  phases 1-3       |  handshake, a few |  replay and MITM  |
|  hits on comments |  (96 in phase 4)  |  ms of compute    |  rejection        |
+-------------------+-------------------+-------------------+-------------------+
|  QUANTUM READINESS BY ROADMAP PHASE (QUANTUMBANK) |  ALSO VALIDATED:          |
|                                                   |                           |
|   100 |                          96.0             |  • Shor simulation factors|
|    80 |                    84.0                   |    15, 21, 143, 221 & 247;|
|    60 |              55.0                         |    peaks match theory.    |
|    40 |        42.0                               |  • ML-KEM/DSA wire sizes  |
|    20 |  33.0                                     |    match FIPS 203/204.    |
|     0 +--------+-------+-------+-------+          |  • Copilot cites only real|
|       Today   Ph 1    Ph 2    Ph 3    Ph 4        |    finding IDs.           |
|                                                   |  • ZIP-slip archives &    |
|                                                   |    unsafe URLs rejected.  |
+---------------------------------------------------+---------------------------+
```

### Slide content
Title: Results and validation: Validated on a seeded bank end to end

Quantitative benchmarks:
- 27 of 27 assets identified: Full recall in QuantumBank across Python, Java, JavaScript, Go, SSH configs, and certificates, with zero hits on comments or documentation.
- 33 -> 84 -> 96 readiness progression: Readiness score recalculates dynamically across the four roadmap phases.
- 8,954 bytes wire footprint: Complete hybrid handshake payload adhering to NIST FIPS 203 and 204 specifications.
- 84 automated tests passing: Complete test suite verifying handshake mechanics, tamper rejection, replay defenses, and API integrity.

Additional verification results:
- Statevector Shor simulation factors 15, 21, 143, 221, and 247; interference peaks match theoretical values.
- Wire footprints match specifications: 1,184 B public key, 1,088 B ciphertext, and 3,309 B signature.
- Copilot validates finding IDs against the database and rejects invalid references.
- ZIP-slip directory traversals and unsafe Git URLs are blocked.

---

## Slide 9: Roadmap: From demo app to real codebases

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  Roadmap: From demo app to real codebases                                     |
+-----------------------+-----------------------+-------------------------------+
|  [ 1 ]                |  [ 2 ]                |  [ 3 ]                        |
|  Deeper discovery     |  Standards & CI       |  Production PQC               |
|                       |                       |                               |
|  • AST and data-flow  |  • CycloneDX CBOM     |  • Hybrid TLS gateway         |
|    analysis across    |    standard export    |    (X25519MLKEM768)           |
|    frameworks         |  • CI gate blocking   |  • PQ / composite certs       |
|  • Binaries and       |    vulnerable crypto  |  • Enterprise KMS & HSM       |
|    container scans    |  • Automated GitHub   |    integration                |
|  • Live TLS/SSH scans |    App remediation PRs|                               |
+-----------------------+-----------------------+-------------------------------+
|  [ 4 ] Real validation                                                        |
|  • Precision/recall benchmarks across 1,000+ public GitHub repositories       |
|  • Enterprise pilot with a partner financial organization                     |
|  • Executing Shor period-finding circuit for N = 15 on IBM Quantum hardware   |
|    using Qiskit                                                               |
+-------------------------------------------------------------------------------+
|  ROUND 2 GOAL: Scan real enterprise repositories with measured accuracy, and   |
|  execute the period-finding circuit on physical quantum hardware.             |
+-------------------------------------------------------------------------------+
```

### Slide content
Title: Roadmap: From demo app to real codebases

1. Deeper discovery:
- AST and data-flow analysis across enterprise frameworks.
- Static scanning of compiled binaries and container images.
- Dynamic network scanning of live TLS and SSH endpoints.

2. Standards and CI integration:
- CycloneDX 1.6 CBOM validation in CI/CD pipelines.
- Security gate blocking pull requests that introduce quantum-vulnerable cryptography.
- Automated GitHub App generating remediation pull requests.

3. Production PQC:
- High-throughput hybrid TLS reverse proxy (X25519MLKEM768).
- Post-quantum and composite X.509 certificate issuance.
- Integration with cloud Key Management Services (AWS KMS, HashiCorp Vault).

4. Real-world validation:
- Precision and recall evaluation on 1,000+ public repositories.
- Enterprise pilot with a partner financial organization.
- Execution of the $N = 15$ period-finding circuit on IBM Quantum hardware via Qiskit.

Round 2 milestone:
Scan enterprise repositories with measured precision and recall, and execute the period-finding circuit on physical quantum hardware.

---

## Slide 10: References and sources

### Layout blueprint
```
+-------------------------------------------------------------------------------+
|  References and Sources                                                       |
+---------------------------------------+---------------------------------------+
|  STANDARDS & RESEARCH                 |  SOFTWARE & DOCUMENTATION             |
|                                       |                                       |
|  • NIST FIPS 203 (ML-KEM), 204        |  • pyca/cryptography: ML-KEM, ML-DSA, |
|    (ML-DSA), 205 (SLH-DSA), Aug 2024  |    AES-GCM, HKDF                      |
|  • NIST IR 8547 (draft): PQC          |  • FastAPI, NumPy, Pydantic, Uvicorn  |
|    Transition Standards, Nov 2024     |  • Anthropic Claude & Google Gemini   |
|  • P.W. Shor, Factorization & Discrete|    APIs (Copilot)                     |
|    Logarithms on a Quantum Computer,  |  • CycloneDX 1.6 CBOM specification   |
|    SIAM J. Computing, 1997            |  • Open Quantum Safe (OQS) project    |
|  • L.K. Grover, Fast Quantum Mechanical|                                      |
|    Database Search, STOC 1996         |                                       |
|  • M. Mosca, Cybersecurity in an Era  |                                       |
|    with Quantum Computers, IEEE 2018  |                                       |
|  • C. Gidney & M. Ekerå, RSA-2048 in  |                                       |
|    8 Hours with 20M Qubits, 2019      |                                       |
|  • C. Gidney, RSA-2048 with <1M       |                                       |
|    Qubits, arXiv:2505.15917           |                                       |
+---------------------------------------+---------------------------------------+
|  ORIGINALITY: Q-SHIELD is our original implementation engineered for           |
|  Q-Hack India 2026. Cryptographic and scientific libraries are consumed as     |
|  dependencies, not forked or copied.                                          |
+-------------------------------------------------------------------------------+
```

### Slide content
Title: References and sources

Standards and research:
- NIST FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM), August 2024.
- NIST FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA), August 2024.
- NIST FIPS 205: Stateless Hash-Based Digital Signature Standard (SLH-DSA), August 2024.
- NIST IR 8547 (Initial Public Draft): Transition to Post-Quantum Cryptography Standards, November 2024.
- P. W. Shor: Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM J. Computing 26(5), 1997.
- L. K. Grover: A fast quantum mechanical algorithm for database search, STOC 1996.
- M. Mosca: Cybersecurity in an era with quantum computers: will we be ready?, IEEE Security & Privacy 16(5), 2018.
- C. Gidney and M. Ekerå: How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits, arXiv:1905.09749, 2019.
- C. Gidney: How to factor 2048 bit RSA integers with less than a million noisy qubits, arXiv:2505.15917, 2025.

Software and specifications:
- pyca/cryptography: ML-KEM, ML-DSA, AES-GCM, and HKDF implementations.
- FastAPI, NumPy, Pydantic, Uvicorn, and SQLite.
- Anthropic Claude and Google Gemini APIs (Security Copilot).
- CycloneDX 1.6 CBOM specification (OWASP / IBM Research).
- Open Quantum Safe (OQS) project.
- Qiskit quantum computing framework.

Originality statement:
Q-SHIELD is our team's original implementation engineered for Q-Hack India 2026. All foundational libraries are consumed strictly as dependencies.
