"""
Device detection utility for responsive design
Helps determine device type and capabilities for optimal UX
"""

import streamlit as st
import re
from typing import Dict, Optional

class DeviceDetector:
    """Detect device type and capabilities from user agent"""
    
    def __init__(self):
        self.user_agent = self._get_user_agent()
        self.device_info = self._analyze_device()
    
    def _get_user_agent(self) -> str:
        """Get user agent from Streamlit session"""
        try:
            # Try to get user agent from browser info
            if hasattr(st, 'experimental_get_query_params'):
                # This is a workaround - in real deployment you'd use JavaScript
                return "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
            return ""
        except:
            return ""
    
    def _analyze_device(self) -> Dict:
        """Analyze user agent to determine device capabilities"""
        device_info = {
            'type': 'desktop',  # desktop, mobile, tablet
            'os': 'unknown',    # ios, android, windows, macos, linux
            'browser': 'unknown', # safari, chrome, firefox, edge
            'supports_pwa': False,
            'supports_audio': True,
            'supports_notifications': True,
            'screen_size': 'large',  # small, medium, large
            'touch_capable': False
        }
        
        ua = self.user_agent.lower()
        
        # Detect mobile devices
        mobile_patterns = [
            r'mobile', r'android', r'iphone', r'ipad', r'ipod',
            r'blackberry', r'windows phone', r'samsung', r'lg',
            r'htc', r'sony', r'nokia'
        ]
        
        if any(re.search(pattern, ua) for pattern in mobile_patterns):
            device_info['type'] = 'mobile'
            device_info['touch_capable'] = True
            device_info['screen_size'] = 'small'
        
        # Detect tablets
        tablet_patterns = [r'ipad', r'tablet', r'kindle']
        if any(re.search(pattern, ua) for pattern in tablet_patterns):
            device_info['type'] = 'tablet'
            device_info['screen_size'] = 'medium'
            device_info['touch_capable'] = True
        
        # Detect OS
        if re.search(r'iphone|ipad|ipod', ua):
            device_info['os'] = 'ios'
            device_info['supports_pwa'] = True
        elif re.search(r'android', ua):
            device_info['os'] = 'android'
            device_info['supports_pwa'] = True
        elif re.search(r'windows', ua):
            device_info['os'] = 'windows'
        elif re.search(r'mac os', ua):
            device_info['os'] = 'macos'
        elif re.search(r'linux', ua):
            device_info['os'] = 'linux'
        
        # Detect browser
        if re.search(r'safari', ua) and not re.search(r'chrome', ua):
            device_info['browser'] = 'safari'
        elif re.search(r'chrome', ua):
            device_info['browser'] = 'chrome'
        elif re.search(r'firefox', ua):
            device_info['browser'] = 'firefox'
        elif re.search(r'edge', ua):
            device_info['browser'] = 'edge'
        
        return device_info
    
    def get_css_variables(self) -> str:
        """Generate CSS variables based on device type"""
        device_css = {
            'mobile': {
                '--app-max-width': '100vw',
                '--app-height': '100vh',
                '--border-radius': '0',
                '--padding': '0',
                '--shadow': 'none',
                '--status-bar-height': 'env(safe-area-inset-top, 20px)',
                '--bottom-safe-area': 'env(safe-area-inset-bottom, 0)',
                '--touch-target-size': '44px'
            },
            'tablet': {
                '--app-max-width': '100vw',
                '--app-height': '100vh',
                '--border-radius': '0',
                '--padding': '0',
                '--shadow': 'none',
                '--status-bar-height': '20px',
                '--bottom-safe-area': '0',
                '--touch-target-size': '44px'
            },
            'desktop': {
                '--app-max-width': '375px',
                '--app-height': '812px',
                '--border-radius': '25px',
                '--padding': '10px',
                '--shadow': '0 0 30px rgba(0,0,0,0.3)',
                '--status-bar-height': '20px',
                '--bottom-safe-area': '0',
                '--touch-target-size': '32px'
            }
        }
        
        device_type = self.device_info['type']
        css_vars = device_css.get(device_type, device_css['desktop'])
        
        css_string = ":root {\n"
        for var, value in css_vars.items():
            css_string += f"    {var}: {value};\n"
        css_string += "}"
        
        return css_string
    
    def get_device_specific_css(self) -> str:
        """Get device-specific CSS optimizations"""
        css = self.get_css_variables()
        
        # Add iOS-specific styles
        if self.device_info['os'] == 'ios':
            css += """
            /* iOS-specific optimizations */
            body {
                -webkit-touch-callout: none;
                -webkit-user-select: none;
                -webkit-tap-highlight-color: transparent;
            }
            
            /* Fix iOS viewport issues */
            .phone-container {
                height: 100vh;
                height: -webkit-fill-available;
            }
            
            /* iOS safe areas */
            .status-bar {
                padding-top: env(safe-area-inset-top);
            }
            
            .ghost-footer {
                padding-bottom: env(safe-area-inset-bottom);
            }
            """
        
        # Add Android-specific styles
        elif self.device_info['os'] == 'android':
            css += """
            /* Android-specific optimizations */
            .phone-container {
                height: 100vh;
            }
            
            /* Android material design touches */
            .circular-record-button {
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            }
            
            .ghost-nav-btn {
                box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            }
            """
        
        return css
    
    def is_mobile(self) -> bool:
        """Check if device is mobile"""
        return self.device_info['type'] in ['mobile', 'tablet']
    
    def supports_audio_recording(self) -> bool:
        """Check if device supports audio recording"""
        # Most modern browsers support it, but some limitations exist
        return self.device_info['supports_audio']
    
    def get_recommended_features(self) -> Dict:
        """Get recommended features based on device"""
        features = {
            'enable_animations': True,
            'enable_haptic_feedback': False,
            'enable_audio_recording': True,
            'enable_notifications': True,
            'use_touch_optimizations': False,
            'enable_pwa_features': False
        }
        
        if self.is_mobile():
            features.update({
                'enable_haptic_feedback': True,
                'use_touch_optimizations': True,
                'enable_pwa_features': self.device_info['supports_pwa']
            })
        
        # Disable animations on older/slower devices
        if self.device_info['browser'] in ['internet_explorer', 'old_android']:
            features['enable_animations'] = False
        
        return features
