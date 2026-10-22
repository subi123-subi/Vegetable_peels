@echo off
title SMART PEEL AI Launcher
cd /d "%~dp0"

echo =========================================================================
echo       SMART PEEL AI -- FULL-PAGE WEB APPLICATION LAUNCHER
echo =========================================================================
echo.

:: 1. Detect dynamic IP and generate portal with QR code
if exist "backend\.venv\Scripts\python.exe" (
    "backend\.venv\Scripts\python.exe" "scripts\generate_gateway.py"
) else (
    python "scripts\generate_gateway.py"
)

echo.
echo [1/2] Launching Python Backend & Full-Page Web Server on Port 8000...
start "SMART PEEL AI - Backend (Port 8000)" cmd /k "run_backend.bat"

echo [2/2] Opening Full-Page Web Application in your browser...
timeout /t 3 /nobreak >nul
start "" "http://localhost:8000"
start "" "connect_portal.html"

echo.
echo =========================================================================
echo SMART PEEL AI Web Application is LIVE!
echo   * Full-Page Web App:   http://localhost:8000 (or http://localhost:8000/kiosk)
echo   * Swagger API Docs:    http://localhost:8000/docs
echo   * Mobile Phone Access: Scan QR code in connect_portal.html
echo =========================================================================
echo.
pause
