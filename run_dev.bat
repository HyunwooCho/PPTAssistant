@echo off
setlocal
cd /d "%~dp0"
python -m pptassistant
if errorlevel 1 py -m pptassistant
pause
