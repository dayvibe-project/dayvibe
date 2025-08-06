@echo off
echo ========================================
echo          DayVibe Landing Page
echo ========================================
echo.
cd /d "C:\Users\JAmbrose\Desktop\Downloads\reflex\streamlit_apps"
echo Checking if we're in the right directory...
dir dayvibe_landing\app.py >nul 2>&1
if errorlevel 1 (
    echo ERROR: Cannot find dayvibe_landing\app.py
    echo Make sure you're running this from the correct directory
    pause
    exit /b 1
)
echo ✓ Found dayvibe_landing\app.py
echo.
echo Starting DayVibe Landing Page...
echo.
echo ⏳ Please wait while the app loads...
echo 🌐 It will open at: http://localhost:8501
echo 📱 Once you see "You can now view your Streamlit app" below,
echo    copy that URL and paste it in your browser
echo.
echo ========================================
echo | dayvibe_env\Scripts\python.exe -m streamlit run dayvibe_landing\app.py --server.port 8501 --server.headless true
echo.
echo ========================================
echo App stopped. Press any key to close...
pause
