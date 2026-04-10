@echo off
cd /d "%~dp0"

REM Launch the UI using pythonw (windowless Python)
pythonw launch-ui.py

REM This batch file will close immediately, leaving the UI running in background
