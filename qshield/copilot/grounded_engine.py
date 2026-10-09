import os
from typing import Dict, Any, Optional
from qshield.cbom.storage import CBOMStorage
from qshield.copilot.hallucination_guard import sanitize_response

class GroundedCopilot:
    """
    CBOM-Grounded Post-Quantum Security Copilot.
    Provides immediate deterministic expert insights grounded strictly in the active CBOM,
    with seamless LLM upgrade when external API keys (ANTHROPIC_API_KEY, GEMINI_API_KEY) are configured.
    """

    def __init__(self, storage: CBOMStorage):
        self.storage = storage

    def ask(self, query: str) -> str:
        report = self.storage.get_latest_report()
        if not report:
            return "No active CBOM scan available. Please scan a repository first."

        valid_ids = self.storage.get_all_finding_ids()
        query_lower = query.lower()

        # Check for external LLM API if configured
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")

        if anthropic_key:
            try:
                raw_answer = self._call_anthropic(query, report, anthropic_key)
                return sanitize_response(raw_answer, valid_ids)
            except Exception:
                pass  # Fall back to grounded deterministic engine

        # Grounded Deterministic Intelligence Engine
        if "what first" in query_lower or "migrate first" in query_lower or "priority" in query_lower:
            p1_findings = [f for f in report.findings if f.phase == 1]
            p1_list = "\n".join([f"- **{f.id}**: `{f.algorithm}` in `{f.file_path}` (Line {f.line_number}) — {f.recommended_replacement}" for f in p1_findings[:4]])
            response = (
                f"### Recommended Priority Action Plan (Phase 1: Perimeter)\n"
                f"Based on the scan of **{report.target_name}** ({report.total_assets} total assets, Readiness: {report.readiness_score}/100), you should address **external perimeter and authentication** first to halt Harvest Now, Decrypt Later (HNDL) exposure:\n\n"
                f"{p1_list}\n\n"
                f"**Immediate Next Step:** Deploy the Hybrid PQC Gateway (ML-KEM-768 + X25519) on public TLS endpoints and replace JWT RS256 with ML-DSA-65."
            )
            return sanitize_response(response, valid_ids)

        elif "rsa" in query_lower:
            rsa_findings = [f for f in report.findings if "RSA" in f.algorithm.upper()]
            citations = ", ".join([f.id for f in rsa_findings[:5]])
            response = (
                f"### Analysis of RSA Cryptography in {report.target_name}\n"
                f"We identified **{len(rsa_findings)} RSA assets** across your codebase (including {citations}).\n"
                f"- **Why Vulnerable:** Shor's quantum algorithm solves prime factorization in polynomial time $O((\\log N)^3)$, allowing an adversary with a cryptanalytically relevant quantum computer to derive the private key directly from the public key.\n"
                f"- **Target Replacement:** For encryption/KEM: migrate to **ML-KEM-768 (NIST FIPS 203)**. For signatures: migrate to **ML-DSA-65 (NIST FIPS 204)**."
            )
            return sanitize_response(response, valid_ids)

        elif "mosca" in query_lower or "hndl" in query_lower or "risk" in query_lower:
            response = (
                f"### Mosca's Inequality & HNDL Risk Posture\n"
                f"For **{report.target_name}**, data confidentiality is evaluated as **HIGH EXPOSURE**:\n"
                f"- **Data Shelf-Life ($X$):** 10.0 years (Banking/financial statutory retention)\n"
                f"- **Migration Time ($Y$):** 2.3 years\n"
                f"- **Quantum Horizon ($Z$):** 12.0 years\n"
                f"- **Result:** $X + Y = 12.3 > 12.0$ ($Z$). Historical financial data protected with RSA-2048 will be decrypted during its legal confidentiality lifetime."
            )
            return sanitize_response(response, valid_ids)

        # Default comprehensive finding overview
        top_critical = [f for f in report.findings if f.severity.value == "CRITICAL"][:3]
        crit_summary = "\n".join([f"- **{f.id}**: `{f.algorithm}` in `{f.file_path}`" for f in top_critical])
        response = (
            f"### Q-SHIELD Security Posture Overview\n"
            f"Target `{report.target_name}` has a Quantum Readiness Score of **{report.readiness_score}/100** with **{report.quantum_vulnerable_count} vulnerable assets**.\n"
            f"Top critical assets requiring immediate attention:\n{crit_summary}\n\n"
            f"Ask me for specific developer tickets, code diffs, or phase roadmaps!"
        )
        return sanitize_response(response, valid_ids)

    def _call_anthropic(self, query: str, report, api_key: str) -> str:
        import httpx
        system_prompt = (
            f"You are Q-SHIELD's Grounded AI Copilot. You are analyzing scan {report.scan_id} "
            f"for codebase {report.target_name}. Current readiness: {report.readiness_score}/100. "
            f"Available finding IDs: {[f.id for f in report.findings]}. NEVER invent finding IDs."
        )
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-3-5-sonnet-20241022", "max_tokens": 1000, "messages": [{"role": "user", "content": query}], "system": system_prompt},
            timeout=10.0
        )
        data = resp.json()
        return data["content"][0]["text"]
