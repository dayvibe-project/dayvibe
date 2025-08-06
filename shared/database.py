import streamlit as st
import os
import sys

# Add shared directory to Python path
shared_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'shared')
if shared_dir not in sys.path:
    sys.path.append(shared_dir)

from supabase_config import supabase_config
import json
from datetime import datetime

def save_signup_email(email: str) -> bool:
    """Save email signup to Supabase"""
    try:
        client = supabase_config.get_client()
        
        # Insert into signups table
        data = {
            "email": email,
            "signup_date": datetime.now().isoformat(),
            "source": "landing_page"
        }
        
        result = client.table("signups").insert(data).execute()
        
        if result.data:
            return True
        else:
            st.error("Failed to save signup")
            return False
            
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return False

def check_email_exists(email: str) -> bool:
    """Check if email already exists in database"""
    try:
        client = supabase_config.get_client()
        
        result = client.table("signups").select("email").eq("email", email).execute()
        
        return len(result.data) > 0
        
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return False
