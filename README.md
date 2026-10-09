# Q-SHIELD: End-to-End Quantum Security Platform
### Discover, Understand, Protect, and Migrate Quantum-Vulnerable Cryptography Before Q-Day
*Track: Enterprise Cybersecurity & Quantum Computing | Event: Q-Hack India 2026*

[![NIST PQC](https://img.shields.io/badge/NIST%20PQC-FIPS%20203%20%7C%20204-0284c7.svg)](https://csrc.nist.gov/pubs/fips/203/final)
[![CycloneDX 1.6](https://img.shields.io/badge/CBOM-CycloneDX%201.6-10B981.svg)](https://cyclonedx.org/capabilities/cbom)
[![Tests](https://img.shields.io/badge/Tests-82%20Passed-10B981.svg)](tests/)
[![Python](https://img.shields.io/badge/Python-3.14-38BDF8.svg)](https://python.org)

## Hackathon deliverables

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| Idea presentation | [`Q-SHIELD.pptx.pdf`](Q-SHIELD.pptx.pdf) and [10-Slide Blueprint](docs/winning_pitch_deck_blueprint.md) | Official 10-slide deck covering problem analysis, Mosca inequality, system design, circuit simulation, and validation. |
| Demo video script | [`docs/demo_video_script.md`](docs/demo_video_script.md) | Three-minute voiceover script and scene guide. |
| Working prototype | `http://127.0.0.1:8000` and [`notebooks/shor_circuit_simulation.ipynb`](notebooks/shor_circuit_simulation.ipynb) | Interactive web console (FastAPI) and runnable Qiskit circuit notebook. |
| Code repository | Current workspace | 82 automated pytest cases, one-click `./run.sh` launcher, and seeded banking benchmark (`QuantumBank`). |

## The migration window

Public-key algorithms such as RSA, Diffie-Hellman, and ECDSA rely on the mathematical difficulty of integer factorization and discrete logarithms. When fault-tolerant quantum hardware reaches adequate scale, Shor's algorithm solves both problems in polynomial time.

Organizations with long-term retention obligations cannot wait for commercial quantum hardware. Adversaries record encrypted network traffic and exfiltrate ciphertexts today to decrypt them once quantum systems mature (harvest now, decrypt later).

### Mosca's inequality

Mosca's inequality defines when migration must begin: data is exposed when $X + Y > Z$.

- $X$ is the required confidentiality lifespan of the data (such as 10 years for financial records under PCI-DSS).
- $Y$ is the operational time required to inventory, refactor, and migrate systems to post-quantum algorithms.
- $Z$ is the estimated time until a quantum computer capable of breaking 2048-bit RSA emerges.

In the included `QuantumBank` test repository:
$$10.0\text{ y } (X) + 2.3\text{ y } (Y) = 12.3\text{ y} > 12.0\text{ y } (Z)$$

The confidentiality requirement outlives the cryptographic protection by several months.

## Platform architecture

```
[ 1. DISCOVER ]  --->  [ 2. UNDERSTAND ]  --->  [ 3. PROTECT ]  --->  [ 4. MIGRATE ]
 Crypto Scanner         Risk and Threat         PQC Gateway          Crypto-Agility
 Polyglot AST/Lexer     Mosca X+Y>Z Model       Hybrid ML-KEM-768    4-Phase Roadmap
 0 Comment False Hits   Exact Shor Simulator    ML-DSA-65 Sigs       Ready-to-Merge Diffs
 CycloneDX 1.6 CBOM     Grover Degradation      AES-256-GCM Secure   Readiness: 33 -> 96

                               [ 5. GROUNDED AI COPILOT ]
                Cites verified finding IDs | Generates Jira tickets | Exports audit reports
```

1. Discovery (Crypto scanner): Polyglot static analysis covering Python, Java, Go, JavaScript, SSH configs, Nginx TLS settings, and X.509 certificates. Code parsers strip comments and docstrings before inspection to eliminate false positives.
2. Risk analysis: Evaluates Mosca deadlines, Grover key degradation, and runs an exact statevector simulation of Shor's algorithm that factors composite moduli ($N \in \{15, 21, 143, 221, 247\}$).
3. Active defense (Hybrid PQC gateway): Reverse proxy combining NIST FIPS 203 (ML-KEM-768) and FIPS 204 (ML-DSA-65) with classical X25519 key exchange. Operates with an 8,954-byte wire handshake, bit-flip tamper rejection, and sliding-window replay protection.
4. Migration engine: Four-phase transition roadmap recalculating organizational readiness from 33 to 96 out of 100, providing contextual code replacement diffs for vulnerable call sites.
5. Grounded security copilot: Query interface connected to the active CBOM database. Validates cited finding IDs against real records, writes Jira and GitHub remediation tickets, and exports compliance summaries.

## Benchmark results

Validated against `benchmarks/quantumbank`, a polyglot banking repository containing intentional cryptographic assets across six file types:

- 27 of 27 seeded cryptographic assets detected across Python, Java, Go, JavaScript, configuration files, and certificates.
- Zero false positive detections from code comments or documentation.
- 8,954 bytes total handshake payload, adhering to FIPS 203 and 204 wire specifications.
- 82 automated test cases passing in under two seconds (`pytest tests/ -v`).
- Five composite moduli factored with exact Fourier peak interference matching ($Q/r = 64$ for $N=15, a=7$).
- Malicious Git clone targets and ZIP-slip directory traversals blocked during scanning.

## Getting started

### Automated startup
```bash
./run.sh
```
This script creates the Python virtual environment, installs project dependencies, runs the test suite, and launches the web interface at `http://127.0.0.1:8000`.

### Manual setup
```bash
# 1. Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3. Run test suite
pytest tests/ -v

# 4. Start the server
uvicorn qshield.main:app --host 0.0.0.0 --port 8000 --reload
```

## Quantum circuit simulation in Jupyter

To inspect the circuit implementation for Deliverable 3:
```bash
source .venv/bin/activate
jupyter notebook notebooks/shor_circuit_simulation.ipynb
```
The notebook demonstrates:
1. Four-qubit modular multiplication circuit in Qiskit.
2. Inverse Quantum Fourier Transform (IQFT) implementation.
3. Measurement histograms and interference peak extraction.
4. Continued fraction expansion for $N = 15$.
5. Gidney-Ekerå resource scaling projections for factoring RSA-2048.

## Interface details

The web console provides:
- Slate dark and Creme light palettes with CSS variable transitions.
- Mathematical canvas rendering an ambient quantum statevector wave in the header.
- Interactive launcher for the QuantumBank repository and ZIP archive dropzone.
- Test harness for the PQC gateway with live bit-flip tamper injection and replay simulations.

## Standards and references

- NIST FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM), August 2024.
- NIST FIPS 204: Module-Lattice-Based Digital Signature Standard (ML-DSA), August 2024.
- NIST IR 8547: Transition to Post-Quantum Cryptography Standards (Draft), November 2024.
- CycloneDX 1.6: Cryptographic Bill of Materials (CBOM) specification, OWASP / IBM Research.
- P. W. Shor: Polynomial-time algorithms for prime factorization on a quantum computer, SIAM J. Comp., 1997.
- C. Gidney and M. Ekerå: How to factor 2048 bit RSA integers in 8 hours using 20M noisy qubits, 2019.
- C. Gidney: How to factor 2048 bit RSA integers with <1M qubits, arXiv:2505.15917, 2025.
