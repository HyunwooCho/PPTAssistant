@echo off
setlocal
cd /d "%~dp0"

echo Building PPTAssistant.exe ...

set "PYTHON_CMD="

for %%P in (python py python3) do (
    if not defined PYTHON_CMD (
        %%P -c "import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
        if not errorlevel 1 set "PYTHON_CMD=%%P"
    )
)

if not defined PYTHON_CMD (
    echo.
    echo A working Python 3.10 or later installation was not found.
    echo Install Python from python.org and enable Add python.exe to PATH.
    pause
    exit /b 1
)

echo Using: %PYTHON_CMD%

%PYTHON_CMD% -m pip install --upgrade pip
if errorlevel 1 goto :fail

%PYTHON_CMD% -m pip install -e ".[dev]"
if errorlevel 1 goto :fail

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist PPTAssistant.spec del /q PPTAssistant.spec

%PYTHON_CMD% -m PyInstaller --noconfirm --clean --onefile --windowed ^
  --name PPTAssistant ^
  --collect-all PySide6 ^
  --paths src ^
  src\pptassistant\main.py
if errorlevel 1 goto :fail

echo.
echo Build completed: dist\PPTAssistant.exe
pause
exit /b 0

:fail
echo.
echo Build failed. Review the error messages above.
pause
exit /b 1
