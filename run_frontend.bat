@echo off
cd /d "%~dp0frontend"
echo ========================================================
echo   Starting SMART PEEL AI Flutter Web on Port 3000
echo ========================================================
echo Localhost URL:    http://localhost:3000
echo Mobile Phone URL: http://192.168.1.35:3000
echo.
flutter run -d web-server --web-port 3000 --web-hostname 0.0.0.0
pause
