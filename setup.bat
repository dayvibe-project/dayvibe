@echo off
echo Setting up DayVibe Streamlit Apps...
echo.

REM Check if Python is installed
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python is installed.
echo.

REM Create virtual environment with project-specific name
echo Creating virtual environment (dayvibe_env)...
py -m venv dayvibe_env
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created.
echo.

REM Activate virtual environment
echo Activating virtual environment...
call dayvibe_env\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
py -m pip install --upgrade pip

REM Install main requirements
echo Installing main dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully.
echo.

REM Copy environment file
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit the .env file with your Supabase credentials!
    echo Open .env and add your SUPABASE_URL and SUPABASE_KEY
    echo.
)

echo Setup complete!
echo.
echo To run the applications:
echo 1. Activate the virtual environment: dayvibe_env\Scripts\activate.bat
echo 2. For DayVibe Landing: cd dayvibe_landing ^&^& streamlit run app.py
echo 3. For DayVibe App: cd dayvibe_app ^&^& streamlit run app.py
echo.
echo Don't forget to configure your Supabase credentials in .env file!
echo.
pause
