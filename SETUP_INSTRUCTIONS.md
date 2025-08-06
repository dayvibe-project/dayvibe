# DayVibe Setup Instructions

## 🚀 Quick Start

### 1. Get Your Supabase Credentials

1. Go to [supabase.com/dashboard](https://supabase.com/dashboard)
2. Select your **DayVibe** project
3. Navigate to **Settings → API**
4. Copy these values:
   - **Project URL** → This is your `NEXT_PUBLIC_SUPABASE_URL`
   - **anon/public key** → This is your `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **service_role key** → This is your `SUPABASE_SERVICE_ROLE_KEY` (for future Next.js backend)

### 2. Configure Environment Variables

Edit the `.env` file in the root directory:

```bash
# Replace with your actual Supabase credentials
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

DEBUG=True
```

### 3. Set Up Database Schema

Run the SQL commands in `supabase_setup.sql` in your Supabase SQL editor:

1. Go to **SQL Editor** in your Supabase dashboard
2. Copy and paste the contents of `supabase_setup.sql`
3. Click **Run**

### 4. Run the Applications

```bash
# Activate virtual environment
dayvibe_env\Scripts\activate.bat

# Run DayVibe Landing Page (port 8501)
cd dayvibe_landing
streamlit run app.py

# Run DayVibe App Interface (port 8502)
cd ..\dayvibe_app
streamlit run app.py --server.port 8502
```

## 🔄 Future Next.js Migration

The environment variables are already named with `NEXT_PUBLIC_` prefix for easy Next.js migration:

- ✅ **Streamlit**: Uses `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- ✅ **Next.js**: Will use the same variable names automatically
- ✅ **Backend APIs**: Will use `SUPABASE_SERVICE_ROLE_KEY` for server-side operations

## 📱 Applications

- **DayVibe Landing**: Email signup page with animated ghost character
- **DayVibe App**: Mobile journaling interface with 2-minute audio recording simulation

## 🛠 Troubleshooting

### Environment Variables Not Loading
- Make sure `.env` file is in the root `streamlit_apps` directory
- Check that there are no extra spaces around the `=` signs
- Restart the Streamlit server after editing `.env`

### Supabase Connection Issues
- Verify your credentials in the Supabase dashboard
- Check that RLS policies are properly set up
- Ensure your project is not paused

### Virtual Environment Issues
```bash
# If activation fails, try:
py -m venv dayvibe_env
dayvibe_env\Scripts\activate.bat
pip install -r requirements.txt
```
