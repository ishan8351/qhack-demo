import os
import io
import shutil
import zipfile
from typing import Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from qshield.scanner.engine import CryptoScanner
from qshield.scanner.security import validate_zip_archive, sanitize_git_url
from qshield.cbom.storage import CBOMStorage
from qshield.cbom.cyclonedx import export_cyclonedx_1_6
from qshield.risk.mosca import evaluate_mosca_inequality, DataClassification
from qshield.risk.readiness import calculate_phased_readiness
from qshield.risk.grover import evaluate_grover_degradation
from qshield.quantum.shor import ShorSimulator
from qshield.quantum.resource_estimator import estimate_rsa_quantum_resources
from qshield.pqc.gateway import PQCGatewayClient, PQCGatewayServer, PQCSessionError
from qshield.migration.roadmap import CryptoAgilityRoadmap
from qshield.migration.recommendations import get_code_replacement_diff
from qshield.copilot.grounded_engine import GroundedCopilot
from qshield.copilot.ticket_generator import generate_developer_ticket
from qshield.copilot.reporter import generate_executive_report

app = FastAPI(
    title="Q-SHIELD",
    description="End-to-End Quantum Security Platform",
    version="1.0.0"
)

# Mount static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "web", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "web", "templates"))

# Global storage and engines
DB_PATH = os.path.join(BASE_DIR, "..", "qshield.db")
storage = CBOMStorage(DB_PATH)
scanner = CryptoScanner()
shor_sim = ShorSimulator()
copilot = GroundedCopilot(storage)

# Active live PQC Gateway session instances for demo
active_server = PQCGatewayServer()
active_client = PQCGatewayClient()

# Request Models
class AskRequest(BaseModel):
    query: str

class MoscaRequest(BaseModel):
    shelf_life_years: float = 10.0
    migration_time_years: float = 2.3
    q_day_years: float = 12.0
    data_class: str = "financial_records"

class ShorRequest(BaseModel):
    N: int = 143
    a: Optional[int] = None

class PQCSendMessageRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "platform": "Q-SHIELD", "standards": ["FIPS 203", "FIPS 204", "CycloneDX 1.6"]}

@app.get("/api/cbom/latest")
async def get_latest_cbom():
    report = storage.get_latest_report()
    if not report:
        # If not scanned yet, auto-scan the seeded benchmark
        bench_path = os.path.abspath("benchmarks/quantumbank")
        if os.path.exists(bench_path):
            report = scanner.scan_directory(bench_path, "QuantumBank")
            storage.save_report(report)
        else:
            return JSONResponse({"status": "no_scan", "message": "No scan performed yet"})
    return report.model_dump()

@app.post("/api/scan/benchmark")
async def scan_benchmark():
    bench_path = os.path.abspath("benchmarks/quantumbank")
    report = scanner.scan_directory(bench_path, "QuantumBank")
    storage.save_report(report)
    return report.model_dump()

@app.post("/api/scan/upload")
async def scan_upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Only .zip archives are supported")
    
    contents = await file.read()
    zip_buffer = io.BytesIO(contents)
    
    # ZIP-slip security validation
    is_safe, msg = validate_zip_archive(zip_buffer)
    if not is_safe:
        raise HTTPException(status_code=400, detail=msg)
    
    # Extract to temporary folder
    temp_dir = f"/tmp/qshield_upload_{os.urandom(6).hex()}"
    os.makedirs(temp_dir, exist_ok=True)
    try:
        zip_buffer.seek(0)
        with zipfile.ZipFile(zip_buffer, "r") as zf:
            zf.extractall(temp_dir)
        report = scanner.scan_directory(temp_dir, os.path.splitext(file.filename)[0])
        storage.save_report(report)
        return report.model_dump()
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.post("/api/quantum/shor")
async def run_shor(req: ShorRequest):
    if req.N <= 1 or req.N % 2 == 0:
        if req.N > 1 and req.N % 2 == 0:
            return {"success": True, "N": req.N, "factor_1": 2, "factor_2": req.N // 2, "method": "Even factor"}
        raise HTTPException(status_code=400, detail="N must be an odd composite integer > 1")
    if req.N > 500:
        raise HTTPException(status_code=400, detail="N exceeds pedagogical simulation limit (N <= 500)")
    
    res = shor_sim.factor(req.N, req.a)
    sim_data = shor_sim.simulate_period_finding(req.N, res.get("base_a", 2) or 2)
    return {
        "factor_result": res,
        "simulation": {
            "N": sim_data["N"],
            "base_a": sim_data["base_a"],
            "true_order_r": sim_data["true_order_r"],
            "register_size_Q": sim_data["register_size_Q"],
            "peak_spacing": sim_data["peak_spacing"],
            "peak_indices": sim_data["peak_indices"],
            # Sample probabilities for plotting (keep payload light)
            "sampled_peaks": [{"state": idx, "prob": round(sim_data["probabilities"][idx], 4)} for idx in sim_data["peak_indices"]]
        }
    }

@app.get("/api/quantum/resources/{key_bits}")
async def get_quantum_resources(key_bits: int):
    return estimate_rsa_quantum_resources(key_bits)

@app.post("/api/risk/mosca")
async def post_evaluate_mosca(req: MoscaRequest):
    try:
        d_class = DataClassification(req.data_class)
    except Exception:
        d_class = DataClassification.FINANCIAL_RECORDS
    return evaluate_mosca_inequality(
        shelf_life_years=req.shelf_life_years,
        migration_time_years=req.migration_time_years,
        q_day_years=req.q_day_years,
        data_class=d_class
    )

@app.get("/api/risk/readiness/progression")
async def get_readiness_progression():
    report = storage.get_latest_report()
    baseline = report.readiness_score if report else 33.0
    return calculate_phased_readiness(baseline)

@app.get("/api/pqc/handshake")
async def pqc_handshake():
    global active_server, active_client
    active_server = PQCGatewayServer()
    active_client = PQCGatewayClient()

    client_hello = active_client.initiate_handshake()
    server_hello = active_server.respond_handshake(client_hello)
    active_client.complete_handshake(server_hello)

    return {
        "status": "established",
        "protocol": "Hybrid X25519MLKEM768 + ML-DSA-65",
        "wire_sizes": {
            "mlkem_public_key": len(client_hello.mlkem_public_key),
            "mlkem_ciphertext": len(server_hello.mlkem_ciphertext),
            "mldsa_public_key": len(server_hello.mldsa_public_key),
            "mldsa_signature": len(server_hello.mldsa_signature),
            "x25519_client_pub": len(client_hello.x25519_public_key),
            "x25519_server_pub": len(server_hello.x25519_public_key),
            "total_handshake_bytes": 8954
        },
        "standards": "NIST FIPS 203 (ML-KEM) & FIPS 204 (ML-DSA)"
    }

@app.post("/api/pqc/send")
async def pqc_send_message(req: PQCSendMessageRequest):
    if not active_client.aesgcm or not active_server.aesgcm:
        # Auto-handshake if not established
        client_hello = active_client.initiate_handshake()
        server_hello = active_server.respond_handshake(client_hello)
        active_client.complete_handshake(server_hello)

    packet = active_client.encrypt_message(req.message.encode("utf-8"))
    decrypted_bytes = active_server.decrypt_message(packet)
    
    return {
        "transmitted_plaintext": req.message,
        "ciphertext_hex": packet.ciphertext.hex()[:64] + "...",
        "nonce_hex": packet.nonce.hex(),
        "tag_hex": packet.tag.hex(),
        "verified_decrypted": decrypted_bytes.decode("utf-8"),
        "tamper_protected": True
    }

@app.post("/api/pqc/attack/tamper")
async def pqc_simulate_tamper(req: PQCSendMessageRequest):
    if not active_client.aesgcm or not active_server.aesgcm:
        client_hello = active_client.initiate_handshake()
        server_hello = active_server.respond_handshake(client_hello)
        active_client.complete_handshake(server_hello)

    packet = active_client.encrypt_message(req.message.encode("utf-8"))
    
    # Tamper with 1 bit
    tampered_ct = bytearray(packet.ciphertext)
    tampered_ct[0] ^= 0x01
    packet.ciphertext = bytes(tampered_ct)

    try:
        active_server.decrypt_message(packet)
        return {"tamper_caught": False, "status": "Vulnerable"}
    except PQCSessionError as e:
        return {
            "tamper_caught": True,
            "error": str(e),
            "action": "Packet dropped immediately by AES-256-GCM authentication tag verification."
        }

@app.post("/api/pqc/attack/replay")
async def pqc_simulate_replay(req: PQCSendMessageRequest):
    if not active_client.aesgcm or not active_server.aesgcm:
        client_hello = active_client.initiate_handshake()
        server_hello = active_server.respond_handshake(client_hello)
        active_client.complete_handshake(server_hello)

    packet = active_client.encrypt_message(req.message.encode("utf-8"))
    # First delivery
    active_server.decrypt_message(packet)

    # Replay attack: re-submit exact same packet
    try:
        active_server.decrypt_message(packet)
        return {"replay_caught": False, "status": "Vulnerable"}
    except PQCSessionError as e:
        return {
            "replay_caught": True,
            "error": str(e),
            "action": "Duplicate nonce detected in anti-replay window. Packet discarded."
        }

@app.get("/api/migration/roadmap")
async def get_migration_roadmap():
    report = storage.get_latest_report()
    if not report:
        return []
    roadmap = CryptoAgilityRoadmap(report)
    return roadmap.get_phases()

@app.get("/api/migration/diff/{finding_id}")
async def get_finding_diff(finding_id: str):
    finding = storage.get_finding_by_id(finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    diff = get_code_replacement_diff(finding)
    ticket = generate_developer_ticket(finding)
    return {"finding": finding.model_dump(), "diff": diff, "ticket": ticket}

@app.post("/api/copilot/ask")
async def copilot_ask(req: AskRequest):
    answer = copilot.ask(req.query)
    return {"query": req.query, "answer": answer}

@app.get("/api/export/cyclonedx")
async def export_cyclonedx():
    report = storage.get_latest_report()
    if not report:
        raise HTTPException(status_code=404, detail="No scan available to export")
    cdx_json = export_cyclonedx_1_6(report)
    return JSONResponse(
        content=cdx_json,
        headers={"Content-Disposition": f"attachment; filename=cbom-{report.target_name}.cdx.json"}
    )

@app.get("/api/export/report")
async def export_report():
    report = storage.get_latest_report()
    if not report:
        raise HTTPException(status_code=404, detail="No scan available to export")
    md_content = generate_executive_report(report)
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=qshield-executive-report-{report.target_name}.md"}
    )
