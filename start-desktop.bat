@echo off
cd /d "%~dp0"

REM Launch the desktop GUI application
python schoolmind_desktop.py

REM This keeps the window open if there's an error
