@echo off
title SMART PEEL AI - Python Backend
cd /d "%~dp0"
echo =========================================================================
echo   Starting SMART PEEL AI FastAPI ^& Neural Classifier (Python Backend)
echo =========================================================================
echo [1] Web Application:   http://localhost:8000
echo [2] Swagger API Docs:  http://localhost:8000/docs
echo [3] Health Endpoint:   http://localhost:8000/health
echo =========================================================================
echo.

timeout /t 2 /nobreak >nul
start "" "http://localhost:8000"

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) else if exist "..\.venv\Scripts\python.exe" (
    "..\.venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
) else (
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
)
pause
