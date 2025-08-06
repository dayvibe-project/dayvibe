import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

class SupabaseConfig:
    def __init__(self):
        # Try Next.js compatible names first, fallback to original names
        self.url = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
        self.key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and ANON KEY must be set in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
    
    def get_client(self) -> Client:
        return self.client

# Global instance
supabase_config = SupabaseConfig()
