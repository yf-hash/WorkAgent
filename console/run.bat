@echo off
cd /d "%~dp0"
echo Starting WorkAgent Console at http://127.0.0.1:8765/
python serverpp.py
pause
