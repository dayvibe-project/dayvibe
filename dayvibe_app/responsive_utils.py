"""
Enhanced responsive utilities for DayVibe app
Provides device detection, responsive CSS generation, and platform-specific optimizations
"""

import streamlit as st
import json
from typing import Dict, Any, Optional
from responsive_config import DEVICE_CSS_VARS, PLATFORM_FEATURES, UI_OPTIMIZATIONS

class ResponsiveManager:
    """Manages responsive design and device-specific features"""
    
    def __init__(self):
        self.device_info = self._get_device_info()
        self._setup_responsive_config()
    
    def _get_device_info(self) -> Dict[str, Any]:
        """Get device information from browser or use defaults"""
        # In a real deployment, you'd use JavaScript to get actual device info
        # For now, we'll use session state or defaults
        
        if 'device_info' not in st.session_state:
            # Default to mobile-first approach
            st.session_state.device_info = {
                'type': 'mobile',  # mobile, tablet, desktop
                'os': 'unknown',   # ios, android, windows, macos
                'screen_width': 375,
                'screen_height': 812,
                'pixel_ratio': 2,
                'supports_touch': True,
                'user_agent': ''
            }
        
        return st.session_state.device_info
    
    def _setup_responsive_config(self):
        """Setup responsive configuration based on device"""
        device_type = self.device_info['type']
        self.css_vars = DEVICE_CSS_VARS.get(device_type, DEVICE_CSS_VARS['mobile'])
        self.ui_opts = UI_OPTIMIZATIONS.get(device_type, UI_OPTIMIZATIONS['mobile'])
    
    def generate_responsive_css(self) -> str:
        """Generate complete responsive CSS"""
        css = f"""
        <style>
        /* Responsive CSS Variables */
        :root {{
            --app-max-width: {self.css_vars['app_max_width']};
            --app-height: {self.css_vars['app_height']};
            --border-radius: {self.css_vars['border_radius']};
            --padding: {self.css_vars['padding']};
            --shadow: {self.css_vars['shadow']};
            --status-bar-height: {self.css_vars['status_bar_height']};
            --bottom-safe-area: {self.css_vars['bottom_safe_area']};
            --touch-target-size: {self.css_vars['touch_target_size']};
            --font-scale: {self.css_vars['font_scale']};
            --spacing-scale: {self.css_vars['spacing_scale']};
        }}
        
        /* Device-specific optimizations */
        {self._get_device_specific_css()}
        
        /* Touch optimizations */
        {self._get_touch_css() if self.device_info['supports_touch'] else ''}
        
        /* Performance optimizations */
        {self._get_performance_css()}
        
        </style>
        """
        return css
    
    def _get_device_specific_css(self) -> str:
        """Get device-specific CSS optimizations"""
        device_os = self.device_info['os']
        
        if device_os == 'ios':
            return """
            /* iOS-specific optimizations */
            body {
                -webkit-touch-callout: none;
                -webkit-user-select: none;
                -webkit-tap-highlight-color: transparent;
            }
            
            .phone-container {
                height: 100vh;
                height: -webkit-fill-available;
            }
            
            .status-bar {
                padding-top: env(safe-area-inset-top);
            }
            
            .ghost-footer {
                padding-bottom: env(safe-area-inset-bottom);
            }
            
            /* iOS button styling */
            .circular-record-button {
                -webkit-appearance: none;
                border: none;
                outline: none;
            }
            """
        
        elif device_os == 'android':
            return """
            /* Android-specific optimizations */
            .phone-container {
                height: 100vh;
            }
            
            /* Material Design touches */
            .circular-record-button {
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
            
            .ghost-nav-btn {
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
            
            /* Android ripple effect */
            .touch-feedback::after {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255,255,255,0.3);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }
            
            .touch-feedback:active::after {
                width: 200px;
                height: 200px;
            }
            """
        
        return ""
    
    def _get_touch_css(self) -> str:
        """Get touch-optimized CSS"""
        return """
        /* Touch optimizations */
        .touch-target {
            min-width: var(--touch-target-size);
            min-height: var(--touch-target-size);
        }
        
        .circular-record-button,
        .ghost-nav-btn,
        .back-button {
            touch-action: manipulation;
            -webkit-touch-callout: none;
            -webkit-user-select: none;
            user-select: none;
        }
        
        /* Improve button feedback */
        .circular-record-button:active {
            transform: scale(0.95);
        }
        
        .ghost-nav-btn:active {
            background: rgba(255,255,255,0.4);
        }
        
        /* Prevent zoom on double tap */
        * {
            touch-action: manipulation;
        }
        """
    
    def _get_performance_css(self) -> str:
        """Get performance-optimized CSS"""
        return """
        /* Performance optimizations */
        .screen {
            will-change: transform;
            transform: translateZ(0);
        }
        
        .avatar-image {
            will-change: transform;
        }
        
        .circular-record-button {
            will-change: transform, box-shadow;
        }
        
        /* Reduce motion for users who prefer it */
        @media (prefers-reduced-motion: reduce) {
            .avatar-image {
                animation: none;
            }
            
            .circular-record-button {
                animation: none;
            }
            
            * {
                transition-duration: 0.01ms !important;
                animation-duration: 0.01ms !important;
            }
        }
        """
    
    def get_button_classes(self) -> str:
        """Get appropriate button classes for the device"""
        classes = ["touch-target"]
        
        if self.ui_opts['enable_touch_feedback']:
            classes.append("touch-feedback")
        
        return " ".join(classes)
    
    def should_enable_feature(self, feature: str) -> bool:
        """Check if a feature should be enabled for this device"""
        device_os = self.device_info['os']
        platform_features = PLATFORM_FEATURES.get(device_os, {})
        
        return platform_features.get(feature, True)
    
    def get_audio_config(self) -> Dict[str, Any]:
        """Get audio configuration for the device"""
        base_config = {
            'sample_rate': 44100,
            'channels': 1,
            'format': 'wav'
        }
        
        # Adjust for device capabilities
        if self.device_info['type'] == 'mobile':
            base_config.update({
                'sample_rate': 22050,  # Lower for mobile to save bandwidth
                'quality': 'medium'
            })
        
        return base_config
    
    def get_pwa_manifest(self) -> Dict[str, Any]:
        """Generate PWA manifest for mobile app experience"""
        return {
            "name": "DayVibe - AI Journaling",
            "short_name": "DayVibe", 
            "description": "Transform your thoughts with AI-powered voice journaling",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#667eea",
            "theme_color": "#667eea",
            "orientation": "portrait-primary",
            "icons": [
                {
                    "src": "/static/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png",
                    "purpose": "maskable any"
                },
                {
                    "src": "/static/icon-512.png", 
                    "sizes": "512x512",
                    "type": "image/png",
                    "purpose": "maskable any"
                }
            ]
        }
    
    def inject_mobile_meta_tags(self) -> str:
        """Generate mobile-optimized meta tags"""
        return """
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="DayVibe">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#667eea">
        
        <!-- PWA Manifest -->
        <link rel="manifest" href="/manifest.json">
        
        <!-- iOS specific -->
        <link rel="apple-touch-icon" href="/static/icon-192.png">
        <link rel="apple-touch-startup-image" href="/static/splash-screen.png">
        
        <!-- Prevent zoom on form inputs -->
        <meta name="format-detection" content="telephone=no">
        """

# Global responsive manager instance
responsive_manager = ResponsiveManager()
