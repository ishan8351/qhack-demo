import pytest
from qshield.scanner.engine import CryptoScanner
from qshield.cbom.storage import CBOMStorage
from qshield.migration.roadmap import CryptoAgilityRoadmap
from qshield.migration.recommendations import get_code_replacement_diff
from qshield.copilot.grounded_engine import GroundedCopilot
from qshield.copilot.hallucination_guard import validate_citations
from qshield.copilot.ticket_generator import generate_developer_ticket
from qshield.copilot.reporter import generate_executive_report

def test_code_replacement_diff_generation():
    """Verify code replacement diffs are generated for findings."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    
    # Test RSA finding diff
    rsa_finding = next(f for f in cbom.findings if "RSA-2048 (Keygen)" in f.algorithm)
    diff = get_code_replacement_diff(rsa_finding)
    assert diff is not None
    assert "-" in diff
    assert "+" in diff
    assert "MLKEM768" in diff or "MLDSA65" in diff or "mlkem" in diff or "mldsa" in diff

    # Test AES finding diff
    aes_finding = next(f for f in cbom.findings if "AES-128" in f.algorithm)
    aes_diff = get_code_replacement_diff(aes_finding)
    assert "AES" in aes_diff
    assert "256" in aes_diff

def test_roadmap_four_phases():
    """Verify 4-phase roadmap partitions findings into phased milestones."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    
    roadmap = CryptoAgilityRoadmap(cbom)
    phases = roadmap.get_phases()
    assert len(phases) == 4
    
    # Phase 1: Perimeter & Auth
    assert phases[0]["phase_num"] == 1
    assert any("TLS" in f.algorithm or "JWT" in f.algorithm or "WebCrypto" in f.algorithm for f in phases[0]["findings"])
    
    # Phase 2: Internal Services
    assert phases[1]["phase_num"] == 2
    assert any("SSH" in f.algorithm or "AES" in f.algorithm for f in phases[1]["findings"])

def test_grounded_copilot_query():
    """Verify grounded copilot answers user questions with real CBOM citations."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    storage = CBOMStorage(":memory:")
    storage.save_report(cbom)
    
    copilot = GroundedCopilot(storage)
    answer = copilot.ask("What should we migrate first in QuantumBank?")
    assert answer is not None
    assert "FIND-" in answer
    assert "Phase 1" in answer or "Perimeter" in answer or "RSA" in answer

def test_hallucination_guard_validates_ids():
    """Verify hallucination guard flags non-existent finding IDs."""
    valid_ids = {"FIND-001", "FIND-002", "FIND-003"}
    
    safe_text = "Remediate FIND-001 and FIND-002 immediately."
    is_grounded, hallucinated = validate_citations(safe_text, valid_ids)
    assert is_grounded is True
    assert len(hallucinated) == 0

    hallucinated_text = "We should also fix FIND-999 and FIND-FAKE in user-service."
    is_grounded, hallucinated = validate_citations(hallucinated_text, valid_ids)
    assert is_grounded is False
    assert "FIND-999" in hallucinated

def test_developer_ticket_generation():
    """Verify Jira/GitHub developer ticket generation."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    finding = cbom.findings[0]
    
    ticket = generate_developer_ticket(finding)
    assert finding.id in ticket
    assert "Title" in ticket or "#" in ticket
    assert "Severity" in ticket
    assert "Recommended Replacement" in ticket
    assert "Code Diff" in ticket or "```" in ticket

def test_executive_report_generation():
    """Verify executive summary report generation."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    report_md = generate_executive_report(cbom)
    assert "Executive Summary" in report_md
    assert "Quantum Readiness Score" in report_md
    assert "Mosca's Inequality" in report_md
    assert "NIST FIPS 203" in report_md
