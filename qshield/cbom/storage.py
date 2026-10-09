import sqlite3
import json
from typing import Optional, List, Set
from datetime import datetime, timezone
from qshield.cbom.schema import CBOMReport, Finding, AssetType, QuantumRisk, Severity

class CBOMStorage:
    """
    SQLite storage engine for Q-SHIELD CBOM reports and individual cryptographic findings.
    Provides persistence and grounding verification for the AI Copilot.
    """

    def __init__(self, db_path: str = "qshield.db"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        return self._conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    scan_id TEXT PRIMARY KEY,
                    target_name TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    total_assets INTEGER NOT NULL,
                    quantum_vulnerable_count INTEGER NOT NULL,
                    readiness_score REAL NOT NULL,
                    metadata TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS findings (
                    id TEXT PRIMARY KEY,
                    scan_id TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    line_number INTEGER NOT NULL,
                    code_snippet TEXT NOT NULL,
                    algorithm TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    quantum_risk TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    description TEXT NOT NULL,
                    recommended_replacement TEXT NOT NULL,
                    phase INTEGER NOT NULL,
                    FOREIGN KEY (scan_id) REFERENCES scans (scan_id)
                )
            """)
            conn.commit()

    def save_report(self, report: CBOMReport):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO scans 
                (scan_id, target_name, timestamp, total_assets, quantum_vulnerable_count, readiness_score, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                report.scan_id,
                report.target_name,
                report.timestamp.isoformat(),
                report.total_assets,
                report.quantum_vulnerable_count,
                report.readiness_score,
                json.dumps(report.metadata)
            ))

            for f in report.findings:
                cursor.execute("""
                    INSERT OR REPLACE INTO findings
                    (id, scan_id, file_path, line_number, code_snippet, algorithm, asset_type, quantum_risk, severity, description, recommended_replacement, phase)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    f.id,
                    report.scan_id,
                    f.file_path,
                    f.line_number,
                    f.code_snippet,
                    f.algorithm,
                    f.asset_type.value,
                    f.quantum_risk.value,
                    f.severity.value,
                    f.description,
                    f.recommended_replacement,
                    f.phase
                ))
            conn.commit()

    def get_latest_report(self) -> Optional[CBOMReport]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM scans ORDER BY timestamp DESC LIMIT 1")
            scan_row = cursor.fetchone()
            if not scan_row:
                return None

            scan_id = scan_row["scan_id"]
            cursor.execute("SELECT * FROM findings WHERE scan_id = ? ORDER BY id ASC", (scan_id,))
            finding_rows = cursor.fetchall()

            findings = [
                Finding(
                    id=row["id"],
                    file_path=row["file_path"],
                    line_number=row["line_number"],
                    code_snippet=row["code_snippet"],
                    algorithm=row["algorithm"],
                    asset_type=AssetType(row["asset_type"]),
                    quantum_risk=QuantumRisk(row["quantum_risk"]),
                    severity=Severity(row["severity"]),
                    description=row["description"],
                    recommended_replacement=row["recommended_replacement"],
                    phase=row["phase"]
                )
                for row in finding_rows
            ]

            return CBOMReport(
                scan_id=scan_row["scan_id"],
                target_name=scan_row["target_name"],
                timestamp=datetime.fromisoformat(scan_row["timestamp"]),
                total_assets=scan_row["total_assets"],
                quantum_vulnerable_count=scan_row["quantum_vulnerable_count"],
                readiness_score=scan_row["readiness_score"],
                findings=findings,
                metadata=json.loads(scan_row["metadata"] or "{}")
            )

    def get_finding_by_id(self, finding_id: str) -> Optional[Finding]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM findings WHERE id = ?", (finding_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Finding(
                id=row["id"],
                file_path=row["file_path"],
                line_number=row["line_number"],
                code_snippet=row["code_snippet"],
                algorithm=row["algorithm"],
                asset_type=AssetType(row["asset_type"]),
                quantum_risk=QuantumRisk(row["quantum_risk"]),
                severity=Severity(row["severity"]),
                description=row["description"],
                recommended_replacement=row["recommended_replacement"],
                phase=row["phase"]
            )

    def get_all_finding_ids(self) -> Set[str]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM findings")
            rows = cursor.fetchall()
            return {row["id"] for row in rows}
