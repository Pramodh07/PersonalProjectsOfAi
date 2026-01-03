# PowerShell helper to start infra and create virtual env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker-compose -f infra/docker-compose.yml up -d
Write-Output "Dev setup complete. Start services with uvicorn e.g., `uvicorn src.ingestor.api:app --reload --port 8000`"