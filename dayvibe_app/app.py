import streamlit as st
import os
import sys
from datetime import datetime, timedelta
import time
import json

# Audio recording imports
try:
    from st_audiorec import st_audiorec
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

# Add shared directory to Python path
shared_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared')
if shared_dir not in sys.path:
    sys.path.append(shared_dir)

def load_mobile_css():
    """Load responsive mobile-first CSS for all devices and platforms"""
    st.markdown("""
    <style>
    /* Reset and base styles */
    .main > div {
        padding: 0;
    }
    
    .stApp {
        background: #f5f5f5;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Responsive variables */
    :root {
        --app-max-width: 100vw;
        --app-height: 100vh;
        --border-radius: 0;
        --padding: 0;
        --shadow: none;
        --status-bar-height: env(safe-area-inset-top, 20px);
        --bottom-safe-area: env(safe-area-inset-bottom, 0);
    }
    
    /* Desktop override - simulate phone */
    @media (min-width: 768px) {
        :root {
            --app-max-width: 375px;
            --app-height: 812px;
            --border-radius: 25px;
            --padding: 10px;
            --shadow: 0 0 30px rgba(0,0,0,0.3);
        }
    }
    
    /* Specific device support */
    /* iPhone SE */
    @media (max-width: 375px) and (max-height: 667px) {
        :root {
            --app-max-width: 100vw;
            --app-height: 100vh;
        }
    }
    
    /* iPhone 12/13/14 */
    @media (max-width: 390px) and (max-height: 844px) {
        :root {
            --app-max-width: 100vw;
            --app-height: 100vh;
        }
    }
    
    /* iPhone 12/13/14 Pro Max */
    @media (max-width: 428px) and (max-height: 926px) {
        :root {
            --app-max-width: 100vw;
            --app-height: 100vh;
        }
    }
    
    /* iPhone 15 Pro */
    @media (max-width: 393px) and (max-height: 852px) {
        :root {
            --app-max-width: 100vw;
            --app-height: 100vh;
        }
    }
    
    /* iPhone 15 Pro Max */
    @media (max-width: 430px) and (max-height: 932px) {
        :root {
            --app-max-width: 100vw;
            --app-height: 100vh;
        }
    }
    
    /* Android devices */
    @media (max-width: 414px) {
        :root {
            --app-max-width: 100vw;
            --app-height: 100vh;
        }
    }
    
    /* Phone container - responsive */
    .phone-container {
        max-width: var(--app-max-width);
        height: var(--app-height);
        margin: 0 auto;
        background: #000;
        border-radius: var(--border-radius);
        padding: var(--padding);
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
    }
    
    .screen {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: calc(var(--border-radius) - var(--padding));
        height: calc(var(--app-height) - 2 * var(--padding));
        overflow: hidden;
        position: relative;
        color: white;
        display: flex;
        flex-direction: column;
    }
    
    /* Status bar - responsive */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: max(var(--status-bar-height), 12px) 20px 12px;
        font-size: clamp(12px, 4vw, 14px);
        font-weight: 600;
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        flex-shrink: 0;
    }
    
    /* Ghost home container - responsive */
    .ghost-home-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: clamp(20px, 8vw, 40px) 20px 20px;
        text-align: center;
        flex-grow: 1;
        justify-content: space-between;
        min-height: 0;
    }
    
    /* Avatar - responsive sizing */
    .ghost-avatar {
        width: clamp(80px, 25vw, 120px);
        height: clamp(80px, 25vw, 120px);
        margin-bottom: clamp(20px, 6vw, 30px);
        position: relative;
        flex-shrink: 0;
    }
    
    .avatar-image {
        width: 100%;
        height: 100%;
        border-radius: 50%;
        border: 4px solid rgba(255,255,255,0.3);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Ghost content - responsive typography */
    .ghost-content {
        margin-bottom: clamp(20px, 8vw, 40px);
        flex-shrink: 0;
    }
    
    .ghost-title {
        font-size: clamp(20px, 7vw, 28px);
        font-weight: 700;
        margin-bottom: 12px;
        color: white;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
        line-height: 1.2;
    }
    
    .ghost-subtitle {
        font-size: clamp(14px, 4vw, 16px);
        opacity: 0.9;
        line-height: 1.4;
        max-width: 90%;
        margin: 0 auto 30px;
    }
    
    /* Quick stats - responsive */
    .quick-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255,255,255,0.15);
        border-radius: clamp(15px, 5vw, 20px);
        padding: clamp(15px, 5vw, 20px);
        margin: 0 auto;
        width: 90%;
        max-width: 320px;
        backdrop-filter: blur(10px);
    }
    
    .stat-item {
        text-align: center;
        flex: 1;
    }
    
    .stat-number {
        display: block;
        font-size: clamp(18px, 6vw, 24px);
        font-weight: 700;
        color: #f6d55c;
        margin-bottom: 4px;
    }
    
    .stat-label {
        font-size: clamp(10px, 3vw, 12px);
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-divider {
        width: 1px;
        height: clamp(30px, 8vw, 40px);
        background: rgba(255,255,255,0.3);
        margin: 0 clamp(10px, 4vw, 15px);
    }
    
    /* Recording section - responsive */
    .recording-feedback {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 5;
    }
    
    .recording-feedback.active {
        opacity: 1;
    }
    
    .recording-timer {
        font-size: clamp(32px, 12vw, 48px);
        font-weight: 700;
        margin-bottom: 10px;
        color: #ff6b6b;
        text-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
    }
    
    .recording-instruction {
        color: rgba(255,255,255,0.8);
        font-size: clamp(12px, 4vw, 14px);
    }
    
    /* Record button section - responsive positioning */
    .record-section {
        position: absolute;
        bottom: clamp(100px, 15vh, 120px);
        left: 50%;
        transform: translateX(-50%);
        z-index: 10;
    }
    
    /* Record button - responsive sizing */
    .circular-record-button {
        width: clamp(60px, 20vw, 80px);
        height: clamp(60px, 20vw, 80px);
        border-radius: 50%;
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        border: 4px solid white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
        touch-action: manipulation;
    }
    
    /* Touch-friendly hover effects */
    @media (hover: hover) {
        .circular-record-button:hover {
            transform: scale(1.1);
            box-shadow: 0 12px 30px rgba(255, 107, 107, 0.4);
        }
    }
    
    /* Touch feedback for mobile */
    .circular-record-button:active {
        transform: scale(0.95);
    }
    
    .circular-record-button.recording {
        background: linear-gradient(135deg, #ff4757, #ff3742);
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3); }
        50% { box-shadow: 0 8px 30px rgba(255, 107, 107, 0.6); }
        100% { box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3); }
    }
    
    .mic-icon {
        width: clamp(24px, 8vw, 32px);
        height: clamp(24px, 8vw, 32px);
        color: white;
    }
    
    /* Footer - responsive positioning */
    .ghost-footer {
        position: absolute;
        bottom: max(var(--bottom-safe-area), 30px);
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 40px);
        max-width: 300px;
    }
    
    /* Navigation button - touch-friendly */
    .ghost-nav-btn {
        background: rgba(255,255,255,0.2);
        border: none;
        border-radius: 15px;
        padding: clamp(12px, 4vw, 15px) 20px;
        color: white;
        font-size: clamp(12px, 4vw, 14px);
        font-weight: 600;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        cursor: pointer;
        transition: background 0.3s ease;
        backdrop-filter: blur(10px);
        min-height: 44px; /* iOS recommended touch target */
        touch-action: manipulation;
    }
    
    @media (hover: hover) {
        .ghost-nav-btn:hover {
            background: rgba(255,255,255,0.3);
        }
    }
    
    .ghost-nav-btn:active {
        background: rgba(255,255,255,0.4);
    }
    
    .ghost-nav-btn svg {
        width: 20px;
        height: 20px;
    }
    
    /* Demo controls */
    .nav-controls {
        text-align: center;
        margin-top: 20px;
        font-size: 14px;
        color: #666;
        font-weight: 500;
    }
    
    /* Progress bar for recording */
    .recording-progress {
        position: absolute;
        bottom: 220px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 4px;
        background: rgba(255,255,255,0.3);
        border-radius: 2px;
        overflow: hidden;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .recording-progress.active {
        opacity: 1;
    }
    
    .progress-fill {
        height: 100%;
        background: #f6d55c;
        border-radius: 2px;
        transition: width 0.1s ease;
    }
    
    /* Journal entries view */
    .entries-view {
        display: none;
        padding: 20px;
        height: calc(100% - 60px);
        overflow-y: auto;
    }
    
    .entries-view.active {
        display: block;
    }
    
    .entries-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .entries-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    
    .entries-subtitle {
        opacity: 0.8;
        font-size: 14px;
    }
    
    .entry-card {
        background: rgba(255,255,255,0.15);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        backdrop-filter: blur(10px);
    }
    
    .entry-date {
        font-size: 12px;
        opacity: 0.7;
        margin-bottom: 8px;
    }
    
    .entry-content {
        font-size: 14px;
        line-height: 1.4;
    }
    
    .entry-mood {
        display: inline-block;
        background: #f6d55c;
        color: #333;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin-top: 10px;
    }
    
    /* Back button */
    .back-button {
        position: absolute;
        top: 70px;
        left: 20px;
        background: rgba(255,255,255,0.2);
        border: none;
        border-radius: 10px;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        backdrop-filter: blur(10px);
    }
    
    .back-button svg {
        width: 20px;
        height: 20px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

def format_time(seconds):
    """Format seconds into MM:SS format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_sample_entries():
    """Get sample journal entries for demo"""
    return [
        {
            "date": "Today, 2:30 PM",
            "content": "Had an interesting conversation with my team about our upcoming project. I realized I've been overthinking the technical implementation when the real challenge is communication.",
            "mood": "Reflective",
            "duration": "1:45"
        },
        {
            "date": "Yesterday, 9:15 AM", 
            "content": "Morning walk was exactly what I needed. Sometimes the best ideas come when you're not trying to force them. Thinking about simplifying our approach.",
            "mood": "Peaceful",
            "duration": "1:12"
        },
        {
            "date": "2 days ago, 6:45 PM",
            "content": "Challenging day at work, but I handled the pressure better than usual. I'm starting to see patterns in how I react to stress. Progress feels slow but it's there.",
            "mood": "Growth",
            "duration": "2:00"
        }
    ]

def main():
    st.set_page_config(
        page_title="DayVibe - AI Journaling App",
        page_icon="👻",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    load_mobile_css()
    
    # Initialize session state
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'home'
    if 'is_recording' not in st.session_state:
        st.session_state.is_recording = False
    if 'recording_time' not in st.session_state:
        st.session_state.recording_time = 0
    if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = get_sample_entries()
    if 'streak_days' not in st.session_state:
        st.session_state.streak_days = 5
    if 'total_entries' not in st.session_state:
        st.session_state.total_entries = 23
    if 'avg_mood' not in st.session_state:
        st.session_state.avg_mood = 4.2
    
    # Phone container with status bar
    st.markdown("""
    <div class="phone-container">
        <div class="screen active" id="ghost-home-screen">
            <div class="status-bar">
                <span>9:41</span>
                <span>100%</span>
            </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.current_view == 'home':
        render_home_screen()
    elif st.session_state.current_view == 'entries':
        render_entries_screen()
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Demo navigation controls
    st.markdown("""
    <div class="nav-controls">
        <span>DayVibe AI Journaling App - Demo</span>
    </div>
    """, unsafe_allow_html=True)

def render_home_screen():
    """Render the main home screen with avatar and recording functionality"""
    
    # Ghost home container
    st.markdown(f"""
    <div class="ghost-home-container">
        <!-- Avatar -->
        <div class="ghost-avatar">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDEyMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIxMjAiIGhlaWdodD0iMTIwIiByeD0iNjAiIGZpbGw9InVybCgjZ3JhZGllbnQwX3JhZGlhbF8xXzIpIi8+CjxjaXJjbGUgY3g9IjQwIiBjeT0iNDUiIHI9IjgiIGZpbGw9IiMzMzMiLz4KPGNpcmNsZSBjeD0iODAiIGN5PSI0NSIgcj0iOCIgZmlsbD0iIzMzMyIvPgo8cGF0aCBkPSJNNDUgNzBRNjAgODUgNzUgNzAiIHN0cm9rZT0iIzMzMyIgc3Ryb2tlLXdpZHRoPSIzIiBmaWxsPSJub25lIi8+CjxkZWZzPgo8cmFkaWFsR3JhZGllbnQgaWQ9ImdyYWRpZW50MF9yYWRpYWxfMV8yIiBjeD0iMCIgY3k9IjAiIHI9IjEiIGdyYWRpZW50VW5pdHM9Im9iamVjdEJvdW5kaW5nQm94Ij4KPHN0b3Agc3RvcC1jb2xvcj0iI0ZGRkZGRiIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNGMEYwRjAiLz4KPC9yYWRpYWxHcmFkaWVudD4KPC9kZWZzPgo8L3N2Zz4K" alt="DayVibe Avatar" class="avatar-image">
        </div>
        
        <div class="ghost-content">
            <h1 class="ghost-title" id="dynamic-title">How's your vibe feeling?</h1>
            <p class="ghost-subtitle" id="dynamic-subtitle">Let's hear you, and transform feelings and thoughts to patterns</p>
            
            <div class="quick-stats">
                <div class="stat-item">
                    <span class="stat-number">{st.session_state.streak_days}</span>
                    <span class="stat-label">Day Streak</span>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-item">
                    <span class="stat-number">{st.session_state.total_entries}</span>
                    <span class="stat-label">Total Entries</span>
                </div>
                <div class="stat-divider"></div>
                <div class="stat-item">
                    <span class="stat-number">{st.session_state.avg_mood}</span>
                    <span class="stat-label">Avg Mood</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Recording feedback section
    recording_class = "active" if st.session_state.is_recording else ""
    st.markdown(f"""
    <div class="recording-feedback {recording_class}" id="recording-feedback">
        <div class="recording-timer" id="recording-timer">{format_time(st.session_state.recording_time)}</div>
        <p class="recording-instruction">Tap to stop recording</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress_class = "active" if st.session_state.is_recording else ""
    progress_percentage = (st.session_state.recording_time / 120) * 100  # 120 seconds = 2 minutes
    st.markdown(f"""
    <div class="recording-progress {progress_class}">
        <div class="progress-fill" style="width: {min(progress_percentage, 100)}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Record button section
    button_class = "recording" if st.session_state.is_recording else ""
    
    # Create columns for centering the record button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if AUDIO_AVAILABLE:
            # Use st_audiorec for actual audio recording
            wav_audio_data = st_audiorec()
            
            if wav_audio_data is not None:
                st.success("Recording saved!")
                # Save audio file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"journal_entry_{timestamp}.wav"
                
                # Create recordings directory if it doesn't exist
                os.makedirs("recordings", exist_ok=True)
                
                with open(f"recordings/{filename}", "wb") as f:
                    f.write(wav_audio_data)
                
                # Add to entries
                new_entry = {
                    "date": datetime.now().strftime("Today, %I:%M %p"),
                    "content": f"Voice recording saved as {filename}",
                    "mood": "Recorded",
                    "duration": "New"
                }
                st.session_state.journal_entries.insert(0, new_entry)
                st.session_state.total_entries += 1
        else:
            # Fallback: simulation button
            if st.button("🎤", key="record_button", help="Start/Stop Recording"):
                if not st.session_state.is_recording:
                    st.session_state.is_recording = True
                    st.session_state.recording_time = 0
                    st.rerun()
                else:
                    st.session_state.is_recording = False
                    st.session_state.recording_time = 0
                    
                    # Add new entry
                    new_entry = {
                        "date": datetime.now().strftime("Today, %I:%M %p"),
                        "content": "Just finished a voice journal session. Feeling good about expressing my thoughts and reflecting on the day.",
                        "mood": "Refreshed",
                        "duration": "2:00"
                    }
                    st.session_state.journal_entries.insert(0, new_entry)
                    st.session_state.total_entries += 1
                    st.success("Journal entry saved!")
                    st.rerun()
    
    # Simulate recording timer
    if st.session_state.is_recording:
        time.sleep(1)
        st.session_state.recording_time += 1
        if st.session_state.recording_time >= 120:  # 2 minutes max
            st.session_state.is_recording = False
            st.session_state.recording_time = 0
        st.rerun()
    
    # Footer navigation
    st.markdown("""
    <div class="ghost-footer">
    """, unsafe_allow_html=True)
    
    # View entries button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 View Past Entries", key="view_entries", use_container_width=True):
            st.session_state.current_view = 'entries'
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_entries_screen():
    """Render the journal entries view"""
    
    # Back button
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("←", key="back_button"):
            st.session_state.current_view = 'home'
            st.rerun()
    
    # Entries view
    st.markdown("""
    <div class="entries-view active">
        <div class="entries-header">
            <h2 class="entries-title">Your Journal</h2>
            <p class="entries-subtitle">Past voice entries and insights</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display entries
    for i, entry in enumerate(st.session_state.journal_entries):
        st.markdown(f"""
        <div class="entry-card">
            <div class="entry-date">{entry['date']}</div>
            <div class="entry-content">{entry['content']}</div>
            <span class="entry-mood">{entry['mood']}</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
