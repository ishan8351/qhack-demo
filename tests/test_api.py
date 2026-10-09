import pytest
from fastapi.testclient import TestClient
from qshield.main import app

client = TestClient(app)

def test_api_index_html():
    res = client.get("/")
    assert res.status_code == 200
    assert "Q-SHIELD" in res.text
    assert "waveCanvas" in res.text

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "FIPS 203" in data["standards"]

def test_api_cbom_latest():
    res = client.get("/api/cbom/latest")
    assert res.status_code == 200
    data = res.json()
    assert data["total_assets"] == 27
    assert data["readiness_score"] == 33.0

def test_api_quantum_shor_simulation():
    res = client.post("/api/quantum/shor", json={"N": 15, "a": 7})
    assert res.status_code == 200
    data = res.json()
    assert data["factor_result"]["success"] is True
    assert {data["factor_result"]["factor_1"], data["factor_result"]["factor_2"]} == {3, 5}
    assert data["simulation"]["peak_spacing"] == 64.0

def test_api_quantum_resources():
    res = client.get("/api/quantum/resources/2048")
    assert res.status_code == 200
    data = res.json()
    assert data["key_size"] == 2048
    assert data["logical_qubits"] > 4000

def test_api_risk_mosca():
    res = client.post("/api/risk/mosca", json={"shelf_life_years": 10.0, "migration_time_years": 2.3, "q_day_years": 12.0})
    assert res.status_code == 200
    data = res.json()
    assert data["is_at_risk"] is True
    assert data["exposure_level"] == "HIGH"

def test_api_pqc_handshake():
    res = client.get("/api/pqc/handshake")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "established"
    assert data["wire_sizes"]["total_handshake_bytes"] == 8954

def test_api_pqc_send_message():
    res = client.post("/api/pqc/send", json={"message": "TEST TRANSACTION"})
    assert res.status_code == 200
    data = res.json()
    assert data["verified_decrypted"] == "TEST TRANSACTION"
    assert data["tamper_protected"] is True

def test_api_pqc_simulate_tamper():
    res = client.post("/api/pqc/attack/tamper", json={"message": "SECURE DATA"})
    assert res.status_code == 200
    data = res.json()
    assert data["tamper_caught"] is True
    assert "dropped" in data["action"].lower()

def test_api_pqc_simulate_replay():
    res = client.post("/api/pqc/attack/replay", json={"message": "REPLAY PACKET"})
    assert res.status_code == 200
    data = res.json()
    assert data["replay_caught"] is True
    assert "duplicate" in data["action"].lower() or "replay" in data["error"].lower()

def test_api_migration_roadmap():
    res = client.get("/api/migration/roadmap")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 4
    assert data[0]["phase_num"] == 1

def test_api_copilot_ask():
    res = client.post("/api/copilot/ask", json={"query": "What should we migrate first?"})
    assert res.status_code == 200
    data = res.json()
    assert "FIND-" in data["answer"]

def test_api_export_cyclonedx():
    res = client.get("/api/export/cyclonedx")
    assert res.status_code == 200
    data = res.json()
    assert data["bomFormat"] == "CycloneDX"
    assert data["specVersion"] == "1.6"

def test_api_export_report():
    res = client.get("/api/export/report")
    assert res.status_code == 200
    assert "text/markdown" in res.headers["content-type"]
    assert "Q-SHIELD Executive" in res.text

def test_api_grover_matrix():
    res = client.get("/api/risk/grover/matrix")
    assert res.status_code == 200
    data = res.json()
    assert len(data) >= 8
    aes128 = next(d for d in data if d["algorithm"] == "AES-128")
    assert aes128["effective_quantum_bits"] == 64
    assert aes128["status"] == "WEAKENED"

def test_api_pqc_simulate_mitm():
    res = client.post("/api/pqc/attack/mitm")
    assert res.status_code == 200
    data = res.json()
    assert data["mitm_caught"] is True
    assert "Signature Verification Failed" in data["error"]

