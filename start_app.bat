@echo off
echo ============================================
echo    Starting AI Model Integrity Verifier
echo ============================================
echo.
echo Make sure Ganache is running in another window!
echo.
call venv\Scripts\activate
cd backend
python app.py