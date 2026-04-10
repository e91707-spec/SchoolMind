@echo off
cd /d "%~dp0"

echo Stopping any existing UI server...
taskkill /f /im python.exe 2>nul
taskkill /f /im pythonw.exe 2>nul

echo Starting fresh UI server...
timeout /t 2 /nobreak >nul

python ui_server.py

pause
