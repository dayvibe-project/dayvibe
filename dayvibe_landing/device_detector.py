"""
Device detection and responsive utilities for DayVibe - Pure Python/Streamlit
"""
import streamlit as st
import re

def detect_device():
    """Detect device type from user agent - Python only"""
    try:
        # Try to get user agent from Streamlit context
        user_agent = ''
        # Streamlit doesn't expose headers directly, so we'll use JavaScript fallback
        # For now, we'll detect based on screen size and other indicators
    except:
        user_agent = ''
    
    device_info = {
        'is_mobile': False,
        'is_tablet': False,
        'is_desktop': True,
        'platform': 'unknown',
        'browser': 'unknown'
    }
    
    # Mobile detection
    mobile_patterns = [
        r'android', r'iphone', r'ipod', r'blackberry', 
        r'windows phone', r'mobile'
    ]
    
    # Tablet detection
    tablet_patterns = [
        r'ipad', r'android.*tablet', r'kindle'
    ]
    
    # Browser detection
    browser_patterns = {
        'chrome': r'chrome',
        'firefox': r'firefox',
        'safari': r'safari',
        'edge': r'edge',
        'opera': r'opera'
    }
    
    # Platform detection
    platform_patterns = {
        'ios': r'iphone|ipad|ipod',
        'android': r'android',
        'windows': r'windows',
        'mac': r'mac os'
    }
    
    if user_agent:
        # Check for tablets first (more specific)
        for pattern in tablet_patterns:
            if re.search(pattern, user_agent):
                device_info['is_tablet'] = True
                device_info['is_desktop'] = False
                break
        
        # Check for mobile if not tablet
        if not device_info['is_tablet']:
            for pattern in mobile_patterns:
                if re.search(pattern, user_agent):
                    device_info['is_mobile'] = True
                    device_info['is_desktop'] = False
                    break
        
        # Detect platform
        for platform, pattern in platform_patterns.items():
            if re.search(pattern, user_agent):
                device_info['platform'] = platform
                break
        
        # Detect browser
        for browser, pattern in browser_patterns.items():
            if re.search(pattern, user_agent):
                device_info['browser'] = browser
                break
    
    return device_info

def get_responsive_config():
    """Get responsive configuration based on device"""
    device = detect_device()
    
    config = {
        'container_width': '100%',
        'font_size_base': '16px',
        'spacing_unit': '1rem',
        'button_size': 'medium',
        'form_layout': 'vertical'
    }
    
    if device['is_mobile']:
        config.update({
            'container_width': '100%',
            'font_size_base': '14px',
            'spacing_unit': '0.8rem',
            'button_size': 'large',
            'form_layout': 'vertical'
        })
    elif device['is_tablet']:
        config.update({
            'container_width': '90%',
            'font_size_base': '15px',
            'spacing_unit': '0.9rem',
            'button_size': 'medium',
            'form_layout': 'vertical'
        })
    
    return config, device

def inject_responsive_css():
    """Inject device-specific CSS"""
    config, device = get_responsive_config()
    
    # Enhanced responsive CSS
    st.markdown(f"""
    <style>
    /* Device-specific optimizations */
    :root {{
        --container-width: {config['container_width']};
        --font-size-base: {config['font_size_base']};
        --spacing-unit: {config['spacing_unit']};
    }}
    
    /* Mobile-first responsive design */
    @media (max-width: 480px) {{
        .hero-title {{ font-size: 2rem !important; }}
        .hero-subtitle {{ font-size: 1rem !important; }}
        .step-card {{ min-width: 100% !important; margin-bottom: 1rem; }}
        .features-grid {{ grid-template-columns: 1fr !important; }}
        
        /* Touch-friendly buttons */
        .stButton > button {{
            height: 3rem !important;
            font-size: 1.1rem !important;
            border-radius: 25px !important;
        }}
        
        /* Better form inputs */
        .stTextInput > div > div > input {{
            height: 3rem !important;
            font-size: 1rem !important;
            border-radius: 25px !important;
        }}
    }}
    
    @media (min-width: 481px) and (max-width: 768px) {{
        .hero-title {{ font-size: 2.5rem !important; }}
        .step-container {{ 
            display: grid !important;
            grid-template-columns: 1fr 1fr !important;
            gap: 1.5rem !important;
        }}
    }}
    
    @media (min-width: 769px) and (max-width: 1024px) {{
        .step-container {{ 
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
        }}
    }}
    
    /* Platform-specific styles */
    {'/* iOS-specific styles */' if device['platform'] == 'ios' else ''}
    {'.stButton > button { -webkit-appearance: none; }' if device['platform'] == 'ios' else ''}
    
    {'/* Android-specific styles */' if device['platform'] == 'android' else ''}
    {'.stTextInput input { outline: none; }' if device['platform'] == 'android' else ''}
    
    /* High DPI displays */
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
        .ghost-body {{ 
            border: 0.5px solid rgba(0,0,0,0.1);
        }}
    }}
    
    /* Landscape orientation for mobile */
    @media (max-width: 768px) and (orientation: landscape) {{
        .hero-container {{ padding: 1.5rem 1rem !important; }}
        .ghost-angel {{ margin: 1rem auto !important; }}
    }}
    
    /* Accessibility improvements */
    @media (prefers-reduced-motion: reduce) {{
        .ghost-angel {{ animation: none !important; }}
        .ghost-halo {{ animation: none !important; }}
    }}
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {{
        /* Already using dark theme, but can adjust if needed */
    }}
    </style>
    """, unsafe_allow_html=True)
    
    return device

def display_device_info():
    """Display device information for debugging"""
    device = detect_device()
    
    if st.checkbox("🔧 Show Device Info (Debug)"):
        st.json({
            "device_type": "Mobile" if device['is_mobile'] else "Tablet" if device['is_tablet'] else "Desktop",
            "platform": device['platform'],
            "browser": device['browser'],
            "is_mobile": device['is_mobile'],
            "is_tablet": device['is_tablet'],
            "is_desktop": device['is_desktop']
        })
