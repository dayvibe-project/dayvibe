# DayVibe Tech Stack - What Needs to Be Changed

## ✅ **Files Already Ready:**
1. **Supabase Integration** - `shared/supabase_config.py` ✅
2. **Landing Page** - `dayvibe_landing/app.py` ✅  
3. **Responsive Design** - `device_detector.py` ✅
4. **Database Functions** - `shared/database.py` ✅

## 🔄 **Files Updated:**
1. **Main Requirements** - `requirements.txt` ✅ Added FastAPI, OpenAI, audio libs
2. **Environment Variables** - `.env.example` ✅ Added OpenAI key
3. **Backend Structure** - Created `backend/` folder ✅

## 🆕 **New Files Created:**
1. **FastAPI Main** - `backend/main.py` ✅
2. **OpenAI Service** - `backend/openai_service.py` ✅  
3. **Audio Processor** - `backend/audio_processor.py` ✅

## 🛠️ **Still Need to Update:**

### 1. **Main Streamlit App** (`dayvibe_app/app.py`)
**Current Issues:**
- Uses mock data instead of real FastAPI calls
- Missing integration with new backend APIs
- Audio recording needs FastAPI integration

**Changes Needed:**
- Replace mock functions with HTTP calls to FastAPI
- Add authentication flow
- Connect voice recording to FastAPI upload endpoint

### 2. **Database Schema** (Supabase)
**Current Issues:**
- Missing tables for new features
- No storage bucket for audio files

**Changes Needed:**
```sql
-- Create missing tables
CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    audio_url TEXT,
    transcription TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'pending'
);

CREATE TABLE ai_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_id UUID REFERENCES journal_entries(id),
    themes JSONB,
    sentiment FLOAT,
    insights TEXT[],
    suggested_goals TEXT[],
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create storage bucket
INSERT INTO storage.buckets (id, name, public) VALUES ('audio-recordings', 'audio-recordings', true);
```

### 3. **Deployment Configuration**
**Need to Create:**
- `backend/requirements.txt` (FastAPI specific)
- `Procfile` for Railway deployment
- `railway.json` configuration
- GitHub Actions for auto-deployment

### 4. **Frontend-Backend Integration**
**Current Issues:**
- Streamlit app doesn't call FastAPI yet
- No error handling for API calls
- Missing loading states

**Changes Needed:**
- Add `httpx` calls to FastAPI endpoints
- Add error handling and retry logic
- Add loading spinners for async operations

## 🚀 **Recommended Next Steps:**

1. **Set up Supabase tables** (create the SQL schema)
2. **Update main Streamlit app** to use FastAPI
3. **Test FastAPI backend** locally
4. **Deploy to Railway** (FastAPI)
5. **Deploy to Streamlit Cloud** (Frontend)
6. **Connect with custom domain**

## 📋 **Commands to Run:**

### Install new dependencies:
```bash
pip install -r requirements.txt
```

### Run FastAPI backend:
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Streamlit frontend:
```bash
streamlit run dayvibe_landing/app.py --server.port 8501
```

### Test the integration:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

Would you like me to start with any specific update first?
