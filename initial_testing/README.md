# Initial Testing Files

This folder contains the test files used during the initial setup and development of DayVibe.

## Files:

### `test_connection.py`
- **Purpose:** Tests Supabase database connection
- **Usage:** `python test_connection.py`
- **What it does:** Verifies that your .env credentials work and can connect to Supabase

### `test_app.py` 
- **Purpose:** Simple Streamlit test application
- **Usage:** `streamlit run test_app.py`
- **What it does:** Basic "Hello World" Streamlit app to verify installation

### `run_test.bat`
- **Purpose:** Batch file to run the test app
- **Usage:** Double-click to run
- **What it does:** Launches test_app.py with proper environment

## When to Use These:

- **Troubleshooting:** If main apps stop working, test with these simple versions
- **New Environment:** When setting up DayVibe on a new computer
- **Development:** For testing new Supabase configurations

## Note:

These files are not needed for normal DayVibe operation. The main applications are:
- `dayvibe_landing/app.py` - Landing page with email signup
- `dayvibe_app/app.py` - Main journaling application
