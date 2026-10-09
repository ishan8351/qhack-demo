import pytest
from qshield.scanner.engine import CryptoScanner

@pytest.fixture(scope="module")
def benchmark_findings():
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    return {f.algorithm: f for f in cbom.findings}

def test_asset_01_server_key(benchmark_findings):
    assert "RSA-2048 (Private Key)" in benchmark_findings

def test_asset_02_server_crt(benchmark_findings):
    assert "RSA-2048 (X.509 Certificate)" in benchmark_findings

def test_asset_03_java_aes_keygen(benchmark_findings):
    assert "AES-128 (Keygen)" in benchmark_findings

def test_asset_04_java_aes_cbc(benchmark_findings):
    assert "AES-128-CBC" in benchmark_findings

def test_asset_05_java_rsa_kpg(benchmark_findings):
    assert "RSA-2048 (KeyPairGen)" in benchmark_findings

def test_asset_06_java_rsa_oaep(benchmark_findings):
    assert "RSA-OAEP" in benchmark_findings

def test_asset_07_java_md5(benchmark_findings):
    assert "MD5" in benchmark_findings

def test_asset_08_java_sha1(benchmark_findings):
    assert "SHA-1" in benchmark_findings

def test_asset_09_go_p256(benchmark_findings):
    assert "ECDSA P-256" in benchmark_findings

def test_asset_10_go_sha256(benchmark_findings):
    assert any("SHA-256" in k for k in benchmark_findings)

def test_asset_11_go_ecdsa_sign(benchmark_findings):
    assert "ECDSA ASN.1 Sign" in benchmark_findings

def test_asset_12_go_ecdsa_verify(benchmark_findings):
    assert "ECDSA ASN.1 Verify" in benchmark_findings

def test_asset_13_go_ecdh(benchmark_findings):
    assert "ECDH P-256" in benchmark_findings

def test_asset_14_js_rsa_oaep(benchmark_findings):
    assert "WebCrypto RSA-OAEP" in benchmark_findings

def test_asset_15_js_rsa_pkcs1(benchmark_findings):
    assert "WebCrypto RSASSA-PKCS1" in benchmark_findings

def test_asset_16_js_jwt_verify(benchmark_findings):
    assert "JWT RS256 Verification" in benchmark_findings

def test_asset_17_py_rsa_keygen(benchmark_findings):
    assert "RSA-2048 (Keygen)" in benchmark_findings

def test_asset_18_py_rsa_sign(benchmark_findings):
    assert "RSA-2048 (Signature)" in benchmark_findings

def test_asset_19_py_rsa_verify(benchmark_findings):
    assert "RSA-2048 (Verification)" in benchmark_findings

def test_asset_20_py_dh(benchmark_findings):
    assert "Diffie-Hellman-2048" in benchmark_findings

def test_asset_21_py_jwt_issue(benchmark_findings):
    assert "JWT RS256 (Issue)" in benchmark_findings

def test_asset_22_py_jwt_decode(benchmark_findings):
    assert "JWT RS256 (Verification)" in benchmark_findings

def test_asset_23_ssh_hostkey(benchmark_findings):
    assert "SSH HostKey ssh-rsa" in benchmark_findings

def test_asset_24_ssh_kex(benchmark_findings):
    assert "SSH Kex Diffie-Hellman" in benchmark_findings

def test_asset_25_tls_ciphers(benchmark_findings):
    assert "TLS ECDHE-RSA CipherSuite" in benchmark_findings

def test_asset_26_tls_protocols(benchmark_findings):
    assert "TLSv1.2 Protocol" in benchmark_findings

def test_asset_27_total_asset_count_exact(benchmark_findings):
    scanner = CryptoScanner()
    cbom = scanner.scan_directory("benchmarks/quantumbank")
    assert len(cbom.findings) == 27
