import os
import io
import zipfile
import pytest
from qshield.scanner.engine import CryptoScanner
from qshield.scanner.security import sanitize_git_url, validate_zip_archive

BENCHMARK_PATH = os.path.abspath("benchmarks/quantumbank")

def test_scanner_discovers_seeded_assets():
    """Verify scanner finds exactly 27 seeded crypto assets in QuantumBank."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory(BENCHMARK_PATH)
    
    assert len(cbom.findings) == 27, f"Expected 27 assets, found {len(cbom.findings)}: {[f.algorithm for f in cbom.findings]}"
    
    # Check that core vulnerable algorithms are detected
    algorithms = [f.algorithm.upper() for f in cbom.findings]
    assert any("RSA" in a for a in algorithms)
    assert any("ECDSA" in a for a in algorithms)
    assert any("ECDH" in a or "DIFFIE-HELLMAN" in a for a in algorithms)
    assert any("AES" in a for a in algorithms)
    assert any("MD5" in a for a in algorithms)
    assert any("SHA-1" in a for a in algorithms)
    assert any("RS256" in a for a in algorithms)

def test_scanner_zero_comment_false_positives():
    """Verify zero hits on commented-out code, docstrings, or documentation files."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory(BENCHMARK_PATH)
    
    # README.md must have 0 findings
    readme_findings = [f for f in cbom.findings if "README.md" in f.file_path]
    assert len(readme_findings) == 0, f"Found false positive in README: {readme_findings}"
    
    # No finding should be inside a comment line
    for finding in cbom.findings:
        line_content = finding.code_snippet.strip()
        assert not line_content.startswith("#"), f"Finding on comment line: {finding.code_snippet}"
        assert not line_content.startswith("//"), f"Finding on comment line: {finding.code_snippet}"
        assert not line_content.startswith("/*"), f"Finding on comment line: {finding.code_snippet}"
        assert not line_content.startswith("*"), f"Finding on comment line: {finding.code_snippet}"

def test_zip_slip_rejection():
    """Verify that malicious archives attempting directory traversal are rejected."""
    # Create an in-memory zip archive containing a zip-slip payload
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("../../etc/passwd", "root:x:0:0:root:/root:/bin/bash")
    
    zip_buffer.seek(0)
    is_valid, msg = validate_zip_archive(zip_buffer)
    assert not is_valid
    assert "directory traversal" in msg.lower() or "zip-slip" in msg.lower()

def test_safe_zip_archive_accepted():
    """Verify that safe zip archives pass validation."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("safe_module/crypto.py", "import os\n")
    
    zip_buffer.seek(0)
    is_valid, msg = validate_zip_archive(zip_buffer)
    assert is_valid

def test_unsafe_git_urls_rejected():
    """Verify that unsafe or malicious Git URLs are rejected."""
    unsafe_urls = [
        "file:///etc/passwd",
        "https://github.com/org/repo.git; rm -rf /",
        "ssh://git@malicious.com/repo.git",
        "http://attacker.com/repo|echo hacked",
        "ftp://repo.com/code.git"
    ]
    for url in unsafe_urls:
        is_safe, _ = sanitize_git_url(url)
        assert not is_safe, f"URL should be rejected: {url}"

def test_safe_git_urls_accepted():
    """Verify that legitimate HTTPS Git URLs are accepted."""
    safe_urls = [
        "https://github.com/QuantumBank/payment-service.git",
        "https://gitlab.com/company/security-repo"
    ]
    for url in safe_urls:
        is_safe, sanitized = sanitize_git_url(url)
        assert is_safe, f"URL should be accepted: {url}"
