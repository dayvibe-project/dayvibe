@echo off
echo ========================================
echo          DayVibe Test
echo ========================================
echo.
cd /d "C:\Users\JAmbrose\Desktop\Downloads\reflex\streamlit_apps"
echo Testing Streamlit installation...
echo.
echo ⏳ Starting test app...
echo 🌐 It will open at: http://localhost:8500
echo.
echo | dayvibe_env\Scripts\python.exe -m streamlit run test_app.py --server.port 8500 --server.headless true
echo.
echo ========================================
echo Test finished. Press any key to close...
pause
