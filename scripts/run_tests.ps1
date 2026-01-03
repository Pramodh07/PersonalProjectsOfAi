# Run tests for the NewProject package from repo root
Push-Location -Path (Join-Path $PSScriptRoot '..\NewProject')
python -m pip install -e .
pytest -q
Pop-Location
