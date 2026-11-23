@echo off
cd /d "%~dp0"
if exist .venv\Scripts\python.exe (
    start "" ".venv\Scripts\python.exe" combined_controller_clean.py
) else (
    python combined_controller_clean.py
)
