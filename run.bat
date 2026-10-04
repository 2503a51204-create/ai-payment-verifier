@echo off
title ProofOfReality AI
echo ========================================
echo      ProofOfReality AI - Starting
echo ========================================
echo.
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Could not install requirements.
    pause
    exit /b 1
)
echo.
echo Starting Flask server...
python app.py
pause
