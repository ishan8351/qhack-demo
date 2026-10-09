import os
import json
import pytest
from qshield.scanner.engine import CryptoScanner
from qshield.cbom.cyclonedx import export_cyclonedx_1_6
from qshield.cbom.storage import CBOMStorage

BENCHMARK_PATH = os.path.abspath("benchmarks/quantumbank")

def test_cyclonedx_export_structure():
    """Verify exported CBOM conforms to CycloneDX 1.6 cryptographic specification."""
    scanner = CryptoScanner()
    cbom = scanner.scan_directory(BENCHMARK_PATH)
    
    cdx = export_cyclonedx_1_6(cbom)
    
    assert cdx["bomFormat"] == "CycloneDX"
    assert cdx["specVersion"] == "1.6"
    assert "serialNumber" in cdx
    assert "metadata" in cdx
    assert "components" in cdx
    assert len(cdx["components"]) == 27
    
    # Check that components are cryptographic-asset
    for comp in cdx["components"]:
        assert comp["type"] == "cryptographic-asset"
        assert "cryptoProperties" in comp
        props = comp["cryptoProperties"]
        assert "assetType" in props
        assert "algorithmProperties" in props
        assert "quantumSecurityLevel" in props or "quantumRisk" in props

def test_sqlite_storage_lifecycle(tmp_path):
    """Verify SQLite persistence: save, load, and finding lookup."""
    db_file = str(tmp_path / "test_cbom.db")
    storage = CBOMStorage(db_file)
    
    scanner = CryptoScanner()
    cbom = scanner.scan_directory(BENCHMARK_PATH)
    
    # Save to SQLite
    storage.save_report(cbom)
    
    # Retrieve report
    loaded_cbom = storage.get_latest_report()
    assert loaded_cbom is not None
    assert loaded_cbom.total_assets == 27
    assert len(loaded_cbom.findings) == 27
    assert loaded_cbom.readiness_score == 33.0
    
    # Lookup individual finding
    finding = storage.get_finding_by_id("FIND-001")
    assert finding is not None
    assert "RSA-2048" in finding.algorithm
    
    # Lookup invalid finding returns None
    assert storage.get_finding_by_id("FIND-999") is None
