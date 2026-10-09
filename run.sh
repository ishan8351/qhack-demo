#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "   ⚛️  Q-SHIELD: End-to-End Quantum Security Platform     "
echo "=========================================================="

# 1. Environment Verification
if [ ! -d ".venv" ]; then
    echo "[+] Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

echo "[+] Activating virtual environment..."
source .venv/bin/activate

# 2. Dependency Check & Install
echo "[+] Checking dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# 3. Test Verification
echo "[+] Running automated test suite (84 tests)..."
pytest tests/ -q

echo "=========================================================="
echo "   🛡️  All tests passing! Starting Q-SHIELD Console...    "
echo "   👉  Open http://127.0.0.1:8000 in your browser         "
echo "=========================================================="

# 4. Launch FastAPI Server
uvicorn qshield.main:app --host 0.0.0.0 --port 8000 --reload
