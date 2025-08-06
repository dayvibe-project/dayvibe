# Responsive Configuration for DayVibe App
# This file contains device-specific settings and responsive design configurations

# Device Breakpoints (in pixels)
DEVICE_BREAKPOINTS = {
    'mobile_small': 320,     # iPhone SE, older Android
    'mobile_medium': 375,    # iPhone 12/13/14
    'mobile_large': 414,     # iPhone Plus models
    'mobile_xl': 430,        # iPhone 15 Pro Max
    'tablet': 768,           # iPad mini
    'tablet_large': 1024,    # iPad Pro
    'desktop': 1200,         # Desktop/laptop
    'desktop_large': 1440    # Large desktop
}

# Device-specific CSS Variables
DEVICE_CSS_VARS = {
    'mobile': {
        'app_max_width': '100vw',
        'app_height': '100vh',
        'border_radius': '0',
        'padding': '0',
        'shadow': 'none',
        'status_bar_height': 'env(safe-area-inset-top, 20px)',
        'bottom_safe_area': 'env(safe-area-inset-bottom, 0)',
        'touch_target_size': '44px',
        'font_scale': '1.0',
        'spacing_scale': '1.0'
    },
    'tablet': {
        'app_max_width': '100vw',
        'app_height': '100vh',
        'border_radius': '0',
        'padding': '0',
        'shadow': 'none',
        'status_bar_height': '20px',
        'bottom_safe_area': '0',
        'touch_target_size': '44px',
        'font_scale': '1.1',
        'spacing_scale': '1.2'
    },
    'desktop': {
        'app_max_width': '375px',
        'app_height': '812px',
        'border_radius': '25px',
        'padding': '10px',
        'shadow': '0 0 30px rgba(0,0,0,0.3)',
        'status_bar_height': '20px',
        'bottom_safe_area': '0',
        'touch_target_size': '32px',
        'font_scale': '1.0',
        'spacing_scale': '1.0'
    }
}

# Platform-specific features
PLATFORM_FEATURES = {
    'ios': {
        'supports_pwa': True,
        'supports_audio': True,
        'supports_notifications': True,
        'supports_haptic': True,
        'requires_user_gesture_audio': True,
        'safe_area_support': True,
        'webkit_optimizations': True
    },
    'android': {
        'supports_pwa': True,
        'supports_audio': True,
        'supports_notifications': True,
        'supports_haptic': True,
        'requires_user_gesture_audio': True,
        'safe_area_support': False,
        'material_design': True
    },
    'windows': {
        'supports_pwa': True,
        'supports_audio': True,
        'supports_notifications': True,
        'supports_haptic': False,
        'requires_user_gesture_audio': False,
        'safe_area_support': False
    },
    'macos': {
        'supports_pwa': True,
        'supports_audio': True,
        'supports_notifications': True,
        'supports_haptic': False,
        'requires_user_gesture_audio': False,
        'safe_area_support': False
    }
}

# Recommended UI optimizations per device
UI_OPTIMIZATIONS = {
    'mobile': {
        'enable_touch_feedback': True,
        'use_large_buttons': True,
        'enable_swipe_gestures': True,
        'minimize_animations': False,
        'use_bottom_navigation': True,
        'enable_pull_refresh': True
    },
    'tablet': {
        'enable_touch_feedback': True,
        'use_large_buttons': True,
        'enable_swipe_gestures': True,
        'minimize_animations': False,
        'use_bottom_navigation': False,
        'enable_pull_refresh': True
    },
    'desktop': {
        'enable_touch_feedback': False,
        'use_large_buttons': False,
        'enable_swipe_gestures': False,
        'minimize_animations': False,
        'use_bottom_navigation': False,
        'enable_pull_refresh': False
    }
}

# Performance settings per device
PERFORMANCE_SETTINGS = {
    'low_end': {
        'enable_animations': False,
        'reduce_image_quality': True,
        'lazy_load_content': True,
        'cache_aggressive': True
    },
    'mid_range': {
        'enable_animations': True,
        'reduce_image_quality': False,
        'lazy_load_content': True,
        'cache_aggressive': False
    },
    'high_end': {
        'enable_animations': True,
        'reduce_image_quality': False,
        'lazy_load_content': False,
        'cache_aggressive': False
    }
}

# Audio recording settings
AUDIO_SETTINGS = {
    'sample_rate': 44100,
    'channels': 1,  # Mono for voice
    'bit_depth': 16,
    'max_duration': 300,  # 5 minutes
    'format': 'wav',
    'compression': 'none'
}

# PWA settings for mobile app-like experience
PWA_CONFIG = {
    'name': 'DayVibe',
    'short_name': 'DayVibe',
    'description': 'AI-powered voice journaling app',
    'theme_color': '#667eea',
    'background_color': '#667eea',
    'display': 'standalone',
    'orientation': 'portrait-primary',
    'start_url': '/',
    'scope': '/',
    'icons': [
        {
            'src': '/static/icon-192.png',
            'sizes': '192x192',
            'type': 'image/png'
        },
        {
            'src': '/static/icon-512.png',
            'sizes': '512x512',
            'type': 'image/png'
        }
    ]
}

# Next.js Migration Planning
NEXTJS_MIGRATION = {
    'framework': 'Next.js 14+',
    'backend': 'tRPC + Prisma',
    'database': 'PostgreSQL (Supabase)',
    'auth': 'NextAuth.js',
    'styling': 'Tailwind CSS + Framer Motion',
    'deployment': 'Vercel',
    'features_to_migrate': [
        'Responsive design system',
        'Audio recording with Web Audio API',
        'Real-time sync',
        'PWA capabilities',
        'Offline support',
        'Push notifications'
    ],
    'estimated_timeline': '4-6 weeks'
}
