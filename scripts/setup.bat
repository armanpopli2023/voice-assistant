@echo off
setlocal enabledelayedexpansion

REM Check if environment name is provided
if "%~1"=="" (
    echo Usage: %0 [development^|production]
    exit /b 1
)

REM Validate environment name
if not "%~1"=="development" if not "%~1"=="production" (
    echo Error: Environment must be either 'development' or 'production'
    exit /b 1
)

set ENV_NAME=%~1
set VENV_PATH=venv_%ENV_NAME%

echo Setting up %ENV_NAME% environment...

REM Create virtual environment if it doesn't exist
if not exist "%VENV_PATH%" (
    echo Creating virtual environment at %VENV_PATH%...
    python -m venv "%VENV_PATH%"
)

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r "requirements\%ENV_NAME%.txt"

REM Install webrtcvad
echo Installing webrtcvad...
pip install webrtcvad

echo Environment setup complete!
echo To activate the environment, run: %VENV_PATH%\Scripts\activate.bat 