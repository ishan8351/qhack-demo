.PHONY: all install test run clean

all: install test

install:
	@echo "Installing dependencies..."
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt

test:
	@echo "Running all 84 automated tests..."
	.venv/bin/pytest tests/ -v

run:
	@echo "Starting Q-SHIELD on http://127.0.0.1:8000..."
	.venv/bin/uvicorn qshield.main:app --host 0.0.0.0 --port 8000 --reload

presentation:
	@echo "Generating 10-slide presentation deck (PPTX and PDF)..."
	.venv/bin/python3 scripts/generate_pptx.py

clean:
	rm -rf __pycache__ .pytest_cache *.db
	find . -type d -name "__pycache__" -exec rm -rf {} +
