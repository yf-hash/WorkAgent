Set-Location $PSScriptRoot
Write-Host "Starting WorkAgent Console at http://127.0.0.1:8765/" -ForegroundColor Cyan
python server/app.py
