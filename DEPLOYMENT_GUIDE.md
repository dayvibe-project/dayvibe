# DayVibe Deployment Guide

## Option 1: Streamlit Community Cloud (FREE - RECOMMENDED)

### Steps:
1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial DayVibe app"
   git remote add origin https://github.com/yourusername/dayvibe-app.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_apps/dayvibe_landing/app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://yourusername-dayvibe-app-streamlit-appsdayvibe-landingapp-xyz123.streamlit.app`

### Required Files:
- `requirements.txt` (already created)
- `app.py` (your main file)

---

## Option 2: Heroku (FREE tier available)

### Setup:
1. **Install Heroku CLI**
2. **Create these files:**

### `Procfile`:
```
web: streamlit run streamlit_apps/dayvibe_landing/app.py --server.port=$PORT --server.address=0.0.0.0
```

### `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

### Deploy commands:
```bash
heroku create your-dayvibe-app
git push heroku main
```

---

## Option 3: GitHub (Multiple Options)

### **3A: GitHub Pages** (Static Sites Only)
- **Cost:** FREE
- **Limitation:** Only static HTML/CSS/JS (not Python/Streamlit)
- **Use for:** Landing page only after converting to static HTML

### **3B: GitHub Codespaces** (Development)
- **Cost:** FREE 60 hours/month, then $0.18/hour
- **Use for:** Development environment, not production hosting
- **Perfect for:** Testing your app before deployment

### **3C: GitHub Actions + External Hosting**
- **Cost:** FREE GitHub Actions + hosting cost
- **How:** Auto-deploy to other platforms when you push code
- **Example workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        run: railway deploy
```

### **3D: GitHub + Streamlit Cloud Integration** (RECOMMENDED)
- **Cost:** FREE
- **How:** GitHub repo → Streamlit Cloud auto-deployment
- **Benefits:** 
  - Push to GitHub → App updates automatically
  - Version control + hosting in one workflow
  - Perfect for your Streamlit app

---

## Option 4: Railway (Modern, Easy)

### Steps:
1. Connect GitHub repo at https://railway.app
2. Select your repository
3. Railway auto-detects Python
4. Set start command: `streamlit run streamlit_apps/dayvibe_landing/app.py --server.port=$PORT`

---

## Option 5: DigitalOcean App Platform

### Steps:
1. Go to https://cloud.digitalocean.com/apps
2. Connect GitHub
3. Select repository
4. Choose Python buildpack
5. Set run command: `streamlit run streamlit_apps/dayvibe_landing/app.py --server.port=$PORT`

---

## Option 6: GoDaddy VPS (If you want to use GoDaddy)

If you specifically want GoDaddy, you'd need their VPS hosting:

### Requirements:
- **GoDaddy VPS** (not shared hosting)
- **Cost:** ~$20-50/month
- **Setup:** Full server management required

### Steps:
1. **Get GoDaddy VPS with Ubuntu**
2. **Install Python & Streamlit:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install streamlit
   ```
3. **Upload your code**
4. **Run with reverse proxy (Nginx)**

---

## Option 7: Custom Domain with Streamlit Cloud

You can use your GoDaddy domain with Streamlit Cloud:

### Steps:
1. Deploy on Streamlit Cloud (free)
2. **In GoDaddy DNS settings:**
   - Add CNAME record: `app` → `your-streamlit-app.streamlit.app`
3. **Access via:** `app.yourdomain.com`

---

## Recommended Approach for You:

### 🎯 **GitHub + Streamlit Cloud (BEST FOR YOUR CASE):**

#### **Step-by-Step Setup:**

1. **Create GitHub Repository:**
   ```bash
   # In your project folder
   git init
   git add .
   git commit -m "Initial DayVibe app"
   
   # Create repo on GitHub.com, then:
   git remote add origin https://github.com/yourusername/dayvibe-app.git
   git branch -M main
   git push -u origin main
   ```

2. **Connect to Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with your GitHub account
   - Click "New app"
   - Select your `dayvibe-app` repository
   - Set main file: `streamlit_apps/dayvibe_landing/app.py`
   - Click "Deploy"

3. **Auto-Deployment Workflow:**
   ```
   Your Code → GitHub → Streamlit Cloud → Live App
   ```
   
   Every time you push to GitHub, your app updates automatically!

4. **Benefits:**
   - ✅ **FREE hosting**
   - ✅ **Automatic deployments** 
   - ✅ **Version control** with GitHub
   - ✅ **Rollback capability** (revert to previous versions)
   - ✅ **Collaboration** (multiple developers)
   - ✅ **Custom domain support**

#### **GitHub Repository Structure:**
```
dayvibe-app/
├── streamlit_apps/
│   ├── dayvibe_landing/
│   │   ├── app.py                 # Main Streamlit app
│   │   ├── responsive_python.py   # Your responsive design
│   │   └── requirements.txt       # Dependencies
│   ├── backend/                   # FastAPI (for Railway)
│   │   ├── main.py
│   │   ├── openai_service.py
│   │   └── audio_processor.py
│   └── shared/                    # Shared utilities
│       ├── database.py
│       └── supabase_config.py
├── .env.example                   # Environment template
├── README.md                      # Project documentation
└── .gitignore                     # Git ignore file
```

#### **Environment Variables on Streamlit Cloud:**
When deploying, add these in Streamlit Cloud dashboard:
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `OPENAI_API_KEY`

### 🚀 **Later upgrade to:**
- **Railway** or **DigitalOcean** for more control
- **AWS/GCP** when you scale up

---

## GitHub-Specific Setup Files:

### 1. `.gitignore`:
```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Streamlit
.streamlit/secrets.toml

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Audio files (if storing locally)
*.wav
*.mp3
*.m4a
```

### 2. `README.md`:
```markdown
# DayVibe - AI Voice Journaling App

Turn everyday thoughts into life-changing goals with 2-minute voice journals + AI-powered insights.

## 🚀 Live Demo
[View App](https://your-dayvibe-app.streamlit.app)

## 🛠️ Tech Stack
- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI 
- **Database:** Supabase
- **AI:** OpenAI (Whisper + GPT-4)
- **Hosting:** Streamlit Cloud + Railway

## 🏃‍♂️ Quick Start
1. Clone the repository
2. Install dependencies: `pip install -r streamlit_apps/requirements.txt`
3. Set up environment variables
4. Run: `streamlit run streamlit_apps/dayvibe_landing/app.py`

## 📱 Features
- Voice recording & transcription
- AI-powered theme detection
- Goal recommendations
- Progress tracking
- Mobile-responsive design
```

### 3. GitHub Actions (Optional - Auto-deploy to Railway):
```yaml
# .github/workflows/deploy-backend.yml
name: Deploy Backend to Railway
on:
  push:
    branches: [main]
    paths: ['streamlit_apps/backend/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Railway CLI
        run: npm install -g @railway/cli
      - name: Deploy to Railway
        run: |
          cd streamlit_apps/backend
          railway deploy
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## Files Needed for Deployment:

### 1. `requirements.txt`:
```
streamlit>=1.28.0
pandas>=1.5.0
python-dateutil>=2.8.0
```

### 2. `.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#764ba2"
secondaryBackgroundColor = "#667eea"
textColor = "#ffffff"
```

### 3. `runtime.txt` (if needed):
```
python-3.9.18
```

---

## Next.js Migration Path:

When you're ready to move to Next.js + tRPC:

### Hosting Options:
1. **Vercel** (best for Next.js) - FREE
2. **Netlify** - FREE tier available  
3. **Railway** - $5/month
4. **GoDaddy shared hosting** ✅ (supports static sites)

### Domain Strategy:
- **Development:** `app.yourdomain.com` (Streamlit)
- **Production:** `yourdomain.com` (Next.js)
