import streamlit as st
import os
import sys
import re
from datetime import datetime, timedelta
from responsive_python import apply_responsive_styles, show_responsive_info, setup_mobile_config

# Add shared directory to Python path
shared_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared')
if shared_dir not in sys.path:
    sys.path.append(shared_dir)

# Only import if dependencies are available
try:
    from database import save_signup_email, check_email_exists
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    st.warning("Supabase not configured. Email signups will be saved locally.")

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_email(email):
    """Clean and normalize email input"""
    if not email:
        return ""
    # Remove whitespace, convert to lowercase, limit length
    email = email.strip().lower()[:255]
    # Remove any potentially dangerous characters
    email = re.sub(r'[<>"\']', '', email)
    return email

def is_rate_limited():
    """Check if user is making too many requests"""
    if 'last_signup_attempt' not in st.session_state:
        return False
    
    if st.session_state.last_signup_attempt:
        time_diff = datetime.now() - st.session_state.last_signup_attempt
        if time_diff < timedelta(seconds=30):  # 30 second cooldown
            return True
    return False

def is_disposable_email(email):
    """Check for common disposable email domains"""
    disposable_domains = [
        '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
        'mailinator.com', 'throwaway.email', '7secure.net'
    ]
    
    if '@' not in email:
        return False
        
    domain = email.split('@')[1].lower()
    return domain in disposable_domains

def secure_signup(email):
    """Enhanced signup with security checks"""
    
    # 1. Check rate limiting first
    if is_rate_limited():
        return False, "⏰ Please wait 30 seconds between signup attempts"
    
    # 2. Sanitize input
    clean_email = sanitize_email(email)
    
    # 3. Validate email format
    if not clean_email:
        return False, "📧 Please enter an email address"
    
    if not validate_email(clean_email):
        return False, "📧 Please enter a valid email address"
    
    # 4. Check for disposable emails (optional warning, not blocking)
    if is_disposable_email(clean_email):
        st.warning("⚠️ Temporary email detected. You might miss important updates!")
    
    # 5. Check email length
    if len(clean_email) > 255:
        return False, "📧 Email address is too long"
    
    # 6. Record attempt time
    st.session_state.last_signup_attempt = datetime.now()
    
    # 7. Save to database
    try:
        if SUPABASE_AVAILABLE:
            success = save_signup_email(clean_email)
        else:
            success = save_email_locally(clean_email)
            
        if success:
            # Track successful signup in session
            if 'successful_signups' not in st.session_state:
                st.session_state.successful_signups = []
            st.session_state.successful_signups.append({
                'email': clean_email,
                'timestamp': datetime.now()
            })
            return True, "🎉 Success! You're on the list for early access!"
        else:
            return False, "💾 This email is already registered!"
    except Exception as e:
        # Log error but don't expose internal details
        print(f"Signup error: {e}")  # This will appear in your server logs
        return False, "⚠️ Something went wrong. Please try again in a moment."

def save_email_locally(email):
    """Fallback: save email to local CSV file"""
    import pandas as pd
    from datetime import datetime
    
    csv_file = "signups.csv"
    
    # Create or append to CSV
    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame(columns=['email', 'signup_date', 'source'])
    
    # Check if email already exists
    if email in df['email'].values:
        return False
    
    # Add new signup
    new_row = pd.DataFrame({
        'email': [email],
        'signup_date': [datetime.now().isoformat()],
        'source': ['landing_page']
    })
    
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(csv_file, index=False)
    return True

def load_custom_css():
    """Load custom CSS for exact design replication"""
    st.markdown("""
    <style>
    /* Reset and base styles */
    .main > div {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Ghost animation styles */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes glow {
        0%, 100% { opacity: 0.8; box-shadow: 0 0 20px rgba(246, 213, 92, 0.6); }
        50% { opacity: 1; box-shadow: 0 0 30px rgba(246, 213, 92, 0.9); }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .ghost-angel {
        display: flex;
        flex-direction: column;
        align-items: center;
        animation: float 3s ease-in-out infinite;
        margin: 2rem auto;
    }
    
    .ghost-halo {
        width: 60px;
        height: 15px;
        background: #f6d55c;
        border-radius: 50%;
        margin-bottom: 10px;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    .ghost-body {
        width: 80px;
        height: 100px;
        background: #ffffff;
        border-radius: 40px 40px 0 0;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .ghost-eyes {
        display: flex;
        gap: 15px;
        margin-bottom: 10px;
    }
    
    .ghost-eye {
        width: 12px;
        height: 12px;
        background: #333;
        border-radius: 50%;
    }
    
    .ghost-smile {
        width: 20px;
        height: 10px;
        border: 2px solid #333;
        border-top: none;
        border-radius: 0 0 20px 20px;
    }
    
    .ghost-tail {
        display: flex;
        margin-top: -5px;
    }
    
    .ghost-tail-part {
        width: 20px;
        height: 30px;
        background: #ffffff;
        margin: 0 -2px;
    }
    
    .ghost-tail-part:nth-child(1) { border-radius: 0 0 20px 0; }
    .ghost-tail-part:nth-child(2) { border-radius: 0 0 0 20px; }
    .ghost-tail-part:nth-child(3) { border-radius: 0 0 20px 0; }
    .ghost-tail-part:nth-child(4) { border-radius: 0 0 0 20px; }
    
    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem;
        color: white;
        animation: fadeInUp 1s ease-out;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        margin-bottom: 2rem;
        opacity: 0.9;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* How it works section */
    .how-it-works {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 1200px;
    }
    
    .step-container {
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        justify-content: center;
        margin-top: 2rem;
    }
    
    .step-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 2rem;
        flex: 1;
        min-width: 300px;
        max-width: 350px;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .step-card:hover {
        transform: translateY(-5px);
    }
    
    .step-number {
        background: #f6d55c;
        color: #4a5568;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0 auto 1rem;
    }
    
    .step-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: white;
    }
    
    .step-description {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    /* Features section */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.25rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: white;
    }
    
    .feature-description {
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.6;
    }
    
    /* Signup section */
    .signup-container {
        background: rgba(74, 85, 104, 0.9);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        max-width: 800px;
        text-align: center;
    }
    
    .signup-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        color: white;
    }
    
    .email-form {
        display: flex;
        flex-direction: column;
        gap: 1rem;
        max-width: 500px;
        margin: 0 auto 2rem;
    }
    
    .email-input {
        padding: 1rem 1.5rem;
        border-radius: 50px;
        border: none;
        font-size: 1.1rem;
        outline: none;
    }
    
    .submit-button {
        background: #f6d55c;
        color: #4a5568;
        padding: 1rem 2rem;
        border-radius: 50px;
        border: none;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .submit-button:hover {
        background: #f6d55c;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(246, 213, 92, 0.4);
    }
    
    /* Trust indicators */
    .trust-indicators {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 2rem;
    }
    
    .trust-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
    }
    
    .trust-icon {
        font-size: 2rem;
        color: #f6d55c;
        margin-bottom: 0.5rem;
    }
    
    .trust-title {
        font-weight: bold;
        color: white;
        margin-bottom: 0.5rem;
    }
    
    .trust-subtitle {
        color: rgba(255, 255, 255, 0.7);
        font-size: 0.9rem;
    }
    
    /* Footer */
    .footer {
        background: #4a5568;
        padding: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 3rem;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .footer-link {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer-link:hover {
        color: white;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .step-container {
            flex-direction: column;
        }
        
        .features-grid {
            grid-template-columns: 1fr;
        }
        
        .email-form {
            max-width: 100%;
        }
        
        .footer-links {
            flex-direction: column;
            gap: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def render_ghost_character():
    """Render the animated ghost character"""
    return """
    <div class="ghost-angel">
        <div class="ghost-halo"></div>
        <div class="ghost-body">
            <div class="ghost-eyes">
                <div class="ghost-eye"></div>
                <div class="ghost-eye"></div>
            </div>
            <div class="ghost-smile"></div>
        </div>
        <div class="ghost-tail">
            <div class="ghost-tail-part"></div>
            <div class="ghost-tail-part"></div>
            <div class="ghost-tail-part"></div>
            <div class="ghost-tail-part"></div>
        </div>
    </div>
    """

def main():
    st.set_page_config(
        page_title="DayVibe - Turn thoughts into life-changing goals",
        page_icon="👻",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Load custom CSS and responsive styles (Pure Python/CSS approach)
    load_custom_css()
    apply_responsive_styles()
    
    # Show responsive info for debugging (optional)
    show_responsive_info()
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-container">
        {render_ghost_character()}
        <h1 class="hero-title">DayVibe</h1>
        <p class="hero-subtitle">Turn everyday thoughts into life‑changing goals with 2‑minute voice journals + AI‑powered insights.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("""
    <div class="how-it-works">
        <h2 style="text-align: center; color: white; font-size: 2.5rem; margin-bottom: 1rem;">How It Works</h2>
        <div class="step-container">
            <div class="step-card">
                <div class="step-number">01</div>
                <div class="step-title">Voice Your Thoughts</div>
                <div class="step-description">
                    • <strong>2‑minute daily voice note</strong><br>
                    • Pause and resume as needed
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">02</div>
                <div class="step-title">AI Surfaces Patterns</div>
                <div class="step-description">
                    • <strong>AI surfaces 5 key themes per week</strong><br>
                    • Emotional themes & opportunity frameworks
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">03</div>
                <div class="step-title">Discover Your Path</div>
                <div class="step-description">
                    • <strong>Get 3 recommended goals tailored to your profile</strong><br>
                    …so you know exactly which goal to chase next.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div style="max-width: 1200px; margin: 2rem auto; padding: 0 1rem;">
        <h2 style="text-align: center; color: white; font-size: 2.5rem; margin-bottom: 2rem;">Core Benefits</h2>
        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🧠</div>
                <div class="feature-title">Insight Frameworks</div>
                <div class="feature-description">
                    Discover which business & life frameworks fit your unique situation.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Goal Alignment</div>
                <div class="feature-description">
                    Turn your organic patterns into actionable, prioritized goals.
                </div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📈</div>
                <div class="feature-title">Trend Tracking</div>
                <div class="feature-description">
                    Track your growth with weekly snapshots and monthly/quarterly trend reports.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Voice Journaling Quote
    st.markdown("""
    <div style="max-width: 800px; margin: 3rem auto; padding: 2rem; background: rgba(255,255,255,0.1); border-radius: 15px; text-align: center;">
        <h3 style="color: white; font-size: 1.5rem; margin-bottom: 1rem;">Voice Journaling in Action</h3>
        <blockquote style="color: rgba(255,255,255,0.9); font-style: italic; font-size: 1.1rem; line-height: 1.6;">
            "Today I realized I dread Monday meetings. But when I said that out loud, DayVibe spotted 'team‑communication gap' as a growth opportunity."
        </blockquote>
        <p style="color: rgba(255,255,255,0.8); margin-top: 1rem;">
            Use everyday conversation—no typing required—to illuminate hidden paths forward.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Signup Section
    st.markdown("""
    <div class="signup-container">
        <h2 class="signup-title">Join the First 200 Early Users</h2>
        <p style="color: rgba(255,255,255,0.9); margin-bottom: 2rem; font-size: 1.1rem;">
            1‑click email signup • Instant confirmation<br>
            Limited to 200 spots
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Email Signup Form
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("signup_form", clear_on_submit=True):
                email = st.text_input(
                    "Email Address",
                    placeholder="Enter your email address",
                    label_visibility="collapsed",
                    key="email_input"
                )
                
                submitted = st.form_submit_button(
                    "Secure My Spot",
                    use_container_width=True,
                    type="primary"
                )
                
                if submitted:
                    if email:
                        success, message = secure_signup(email)
                        if success:
                            st.success(message)
                            st.balloons()
                        else:
                            st.error(message)
                    else:
                        st.error("📧 Please enter your email address.")
    
    # Trust Indicators
    st.markdown("""
    <div style="max-width: 800px; margin: 2rem auto;">
        <div class="trust-indicators">
            <div class="trust-item">
                <div class="trust-icon">✅</div>
                <div class="trust-title">Beta Access</div>
                <div class="trust-subtitle">Early features</div>
            </div>
            <div class="trust-item">
                <div class="trust-icon">💎</div>
                <div class="trust-title">Lifetime Discount</div>
                <div class="trust-subtitle">50% off forever</div>
            </div>
            <div class="trust-item">
                <div class="trust-icon">🛡️</div>
                <div class="trust-title">GDPR Compliant</div>
                <div class="trust-subtitle">EU‑approved</div>
            </div>
            <div class="trust-item">
                <div class="trust-icon">🔒</div>
                <div class="trust-title">100% Private</div>
                <div class="trust-subtitle">No sharing. Ever.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-links">
            <a href="#" class="footer-link">Privacy Policy</a>
            <a href="#" class="footer-link">Terms of Service</a>
            <a href="#" class="footer-link">Contact</a>
        </div>
        <p>&copy; 2025 DayVibe. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
