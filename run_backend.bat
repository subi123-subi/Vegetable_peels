@echo off
cd /d "%~dp0backend"
echo ========================================================
echo   Starting SMART PEEL AI FastAPI Backend on Port 8000
echo ========================================================
echo API Swagger Docs: http://localhost:8000/docs
echo Network API URL:  http://192.168.1.35:8000/docs
echo.
".venv\Scripts\python.exe" -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
