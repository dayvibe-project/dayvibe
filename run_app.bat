@echo off
cd /d "C:\Users\JAmbrose\Desktop\Downloads\reflex\streamlit_apps"
echo Starting DayVibe App Interface...
echo Open your browser to: http://localhost:8502
echo | dayvibe_env\Scripts\python.exe -m streamlit run dayvibe_app\app.py --server.port 8502 --server.headless true
pause
