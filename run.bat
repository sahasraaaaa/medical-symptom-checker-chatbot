@echo off
REM Quick start script for Windows

echo ============================================================
echo Medical Symptom Checker Chatbot
echo ============================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Check if model exists
if not exist "models\disease_model.pkl" (
    echo Model not found. Running setup...
    python setup.py
    echo.
)

REM Start the application
echo Starting Medical Symptom Checker Chatbot...
echo Open your browser and navigate to: http://localhost:5000
echo.
echo Press CTRL+C to stop the server.
echo ============================================================
echo.

python app.py

pause
