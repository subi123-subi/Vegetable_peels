@echo off
title SMART PEEL AI - Full-Page Web App (HTML/CSS/JS)
cd /d "%~dp0"
echo =========================================================================
echo   Launching SMART PEEL AI Full-Page Web App (HTML / CSS / JavaScript)
echo =========================================================================
echo Directory: %~dp0
echo.
echo Starting local web server on http://localhost:5500 ...
echo Opening Full-Page Web App in your default browser...
start "" "http://localhost:5500"

if exist "..\backend\.venv\Scripts\python.exe" (
    "..\backend\.venv\Scripts\python.exe" -m http.server 5500 --bind 127.0.0.1
) else (
    python -m http.server 5500 --bind 127.0.0.1 2>nul || (
        echo Fallback: Opening index.html directly in browser...
        start "" "index.html"
    )
)
pause
