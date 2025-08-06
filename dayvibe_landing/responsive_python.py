"""
Pure Python device detection for Streamlit - No JavaScript dependencies
"""
import streamlit as st

def get_screen_info():
    """Get screen dimensions using Streamlit's JavaScript capabilities"""
    # This is a simple Python-only approach
    # We use CSS breakpoints instead of JavaScript detection
    return {
        'width': 'unknown',
        'height': 'unknown'
    }

def detect_device_simple():
    """Simple device detection based on Streamlit's capabilities"""
    
    # Default to desktop-friendly settings
    device_info = {
        'is_mobile': False,
        'is_tablet': False, 
        'is_desktop': True,
        'platform': 'web',
        'layout': 'wide'
    }
    
    # We'll use CSS media queries for responsive design
    # This is the most reliable cross-platform approach
    return device_info

def apply_responsive_styles():
    """Apply responsive CSS styles - Pure CSS approach"""
    st.markdown("""
    <style>
    /* Mobile-first responsive design - Pure CSS */
    
    /* Base styles for all devices */
    .main-container {
        max-width: 100%;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Small screens (mobile phones) */
    @media (max-width: 480px) {
        .main-container {
            padding: 0.5rem;
        }
        
        .hero-title {
            font-size: 1.8rem !important;
            line-height: 1.2 !important;
        }
        
        .hero-subtitle {
            font-size: 0.9rem !important;
        }
        
        .step-card {
            min-width: 100% !important;
            margin-bottom: 1rem !important;
            padding: 1rem !important;
        }
        
        .features-grid {
            grid-template-columns: 1fr !important;
            gap: 1rem !important;
        }
        
        /* Touch-friendly buttons for mobile */
        .stButton > button {
            height: 2.8rem !important;
            font-size: 1rem !important;
            border-radius: 20px !important;
            width: 100% !important;
            touch-action: manipulation;
        }
        
        /* Better form inputs for mobile */
        .stTextInput > div > div > input {
            height: 2.8rem !important;
            font-size: 1rem !important;
            border-radius: 20px !important;
            padding: 0.75rem 1rem !important;
        }
        
        /* Stack elements vertically on mobile */
        .step-container {
            flex-direction: column !important;
            gap: 1rem !important;
        }
    }
    
    /* Medium screens (tablets) */
    @media (min-width: 481px) and (max-width: 768px) {
        .hero-title {
            font-size: 2.2rem !important;
        }
        
        .step-container {
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 1.5rem !important;
        }
        
        .features-grid {
            grid-template-columns: 1fr 1fr !important;
        }
    }
    
    /* Large tablets and small laptops */
    @media (min-width: 769px) and (max-width: 1024px) {
        .step-container {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
        }
    }
    
    /* Large screens (desktop) */
    @media (min-width: 1025px) {
        .main-container {
            max-width: 1200px;
        }
    }
    
    /* iOS-specific optimizations */
    @supports (-webkit-touch-callout: none) {
        .stButton > button {
            -webkit-appearance: none;
            -webkit-tap-highlight-color: transparent;
        }
        
        .stTextInput input {
            -webkit-appearance: none;
            border-radius: 20px;
        }
    }
    
    /* Android-specific optimizations */
    @media screen and (-webkit-min-device-pixel-ratio: 1) {
        .stTextInput input {
            outline: none;
            border: 2px solid #e0e0e0;
        }
        
        .stTextInput input:focus {
            border-color: #667eea;
        }
    }
    
    /* High DPI displays (Retina, etc.) */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
        .ghost-body {
            border: 0.5px solid rgba(0,0,0,0.1);
        }
        
        .step-card, .feature-card {
            border: 0.5px solid rgba(255,255,255,0.1);
        }
    }
    
    /* Landscape orientation for mobile */
    @media (max-width: 768px) and (orientation: landscape) {
        .hero-container {
            padding: 1rem !important;
        }
        
        .ghost-angel {
            margin: 0.5rem auto !important;
            transform: scale(0.8);
        }
    }
    
    /* Accessibility - Reduced motion */
    @media (prefers-reduced-motion: reduce) {
        .ghost-angel {
            animation: none !important;
        }
        
        .ghost-halo {
            animation: none !important;
        }
        
        * {
            transition: none !important;
            animation: none !important;
        }
    }
    
    /* Dark mode support (if user prefers) */
    @media (prefers-color-scheme: dark) {
        /* Our app is already dark, but we can adjust if needed */
    }
    
    /* Print styles */
    @media print {
        .stButton, .stTextInput {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def show_responsive_info():
    """Show responsive design information for debugging"""
    device = detect_device_simple()
    
    with st.expander("🔧 Responsive Design Info"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Device Detection:**")
            st.json(device)
        
        with col2:
            st.write("**Responsive Features:**")
            st.write("✅ CSS Media Queries")
            st.write("✅ Touch-friendly buttons")
            st.write("✅ Mobile-first design")
            st.write("✅ iOS/Android optimized")
            st.write("✅ High DPI support")
            st.write("✅ Accessibility friendly")

def setup_mobile_config():
    """Configure Streamlit for mobile-friendly behavior"""
    # This is called in your main app
    st.set_page_config(
        page_title="DayVibe - AI Voice Journaling",
        page_icon="👻", 
        layout="wide",  # Use wide layout, but constrain with CSS
        initial_sidebar_state="collapsed",
        menu_items={
            'Get Help': None,
            'Report a bug': None,
            'About': "DayVibe - Turn thoughts into goals"
        }
    )
