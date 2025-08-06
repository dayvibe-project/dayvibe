# Streamlit Apps - DayVibe

This repository contains two separate Streamlit applicat#### DayVibe App:
```bash
# Activate environment first  
dayvibe_env\Scripts\activate  # Windows
# or source dayvibe_env/bin/activate  # macOS/Linux

cd dayvibe_app
streamlit run app.py
```## 1. DayVibe Landing Page (`dayvibe_landing/`)
A conversion of the React/TypeScript landing page to Streamlit with:
- Exact visual design replication
- Animated ghost character
- Email signup with Supabase backend
- Responsive design
- Trust indicators and features section

## 2. DayVibe App (`dayvibe_app/`)
A mobile-first journaling interface with:
- Exact UI replication from HTML mockup
- Real audio recording (2-minute max)
- Journal entries management
- Mobile phone-like interface
- Recording timer and progress bar

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone and navigate to the project:**
```bash
cd streamlit_apps
```

2. **Create virtual environment:**
```bash
python -m venv dayvibe_env
dayvibe_env\Scripts\activate  # Windows
# or
source dayvibe_env/bin/activate  # macOS/Linux
```

3. **Install dependencies:**
```bash
# For both apps (main requirements)
pip install -r requirements.txt

# Or install individually
pip install -r dayvibe_landing/requirements.txt
pip install -r dayvibe_app/requirements.txt
```

### Supabase Configuration

1. **Create a Supabase project** at https://supabase.com
2. **Create the signups table:**
```sql
CREATE TABLE signups (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    signup_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source VARCHAR(50) DEFAULT 'landing_page'
);
```

3. **Setup environment variables:**
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your Supabase credentials
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### Running the Applications

#### DayVibe Landing Page:
```bash
# Activate environment first
venv_dayvibe\Scripts\activate  # Windows
# or source venv_dayvibe/bin/activate  # macOS/Linux

cd dayvibe_landing
streamlit run app.py
```

#### Reflekt App:
```bash
# Activate environment first  
venv_dayvibe\Scripts\activate  # Windows
# or source venv_dayvibe/bin/activate  # macOS/Linux

cd reflekt_app
streamlit run app.py
```

The applications will be available at:
- DayVibe Landing: http://localhost:8501
- DayVibe App: http://localhost:8502 (if running simultaneously)

## Features

### DayVibe Landing Page
- ✅ Exact visual design replication
- ✅ Animated floating ghost character
- ✅ Responsive design (mobile & desktop)
- ✅ Email validation and signup
- ✅ Supabase backend integration
- ✅ Local fallback (CSV) if Supabase unavailable
- ✅ Trust indicators section
- ✅ "How It Works" process flow
- ✅ Core benefits showcase

### DayVibe App
- ✅ Mobile-first interface design
- ✅ Exact UI replication from HTML mockup
- ✅ Phone container with status bar
- ✅ Real audio recording (st-audiorec)
- ✅ 2-minute recording limit with progress bar
- ✅ Recording timer display
- ✅ Journal entries management
- ✅ Navigation between home and entries
- ✅ Sample journal entries for demo
- ✅ Statistics tracking (streak, total entries, avg mood)

## File Structure
```
streamlit_apps/
├── requirements.txt           # Main dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
├── shared/                   # Shared utilities
│   ├── supabase_config.py   # Supabase client configuration
│   └── database.py          # Database operations
├── dayvibe_landing/          # Landing page app
│   ├── app.py               # Main Streamlit app
│   ├── requirements.txt     # Specific dependencies
│   └── signups.csv          # Local backup (created automatically)
└── dayvibe_app/             # Journaling interface app
    ├── app.py               # Main Streamlit app
    ├── requirements.txt     # Specific dependencies
    └── recordings/          # Audio recordings folder (created automatically)
```

## Deployment

Both apps can be deployed to Streamlit Cloud:

1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Add environment variables in Streamlit Cloud settings
4. Deploy each app separately using the respective app.py files

## Audio Recording Notes

The DayVibe app uses `st-audiorec` for real audio recording. If the package is not available, it falls back to a simulation mode with mock recordings. The audio files are saved in the `recordings/` directory with timestamps.

## Troubleshooting

### Supabase Connection Issues
- Verify your Supabase URL and key in the `.env` file
- Check that the `signups` table exists in your database
- Ensure RLS (Row Level Security) policies allow inserts if enabled

### Audio Recording Issues
- Make sure microphone permissions are granted in your browser
- Try refreshing the page if audio recording doesn't work initially
- Check browser console for any WebRTC-related errors

### CSS/Styling Issues
- The apps use extensive custom CSS for exact design replication
- Clear browser cache if styles appear broken
- Ensure Streamlit version is 1.28.0 or higher

## Development

To modify the designs:
- DayVibe Landing: Edit the `load_custom_css()` function in `dayvibe_landing/app.py`
- DayVibe App: Edit the `load_mobile_css()` function in `dayvibe_app/app.py`

Both apps preserve the exact visual design from the original React/HTML implementations.
