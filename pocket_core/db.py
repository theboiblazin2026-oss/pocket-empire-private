import streamlit as st
from supabase import create_client, Client
import os

# Singleton pattern for DB connection
_supabase_client = None

def get_db():
    global _supabase_client
    
    # Try getting from Streamlit secrets (Cloud)
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY")
    
    # Fallback to env vars (Local)
    if not url: url = os.getenv("SUPABASE_URL")
    if not key: key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        return None

    try:
        if _supabase_client is None:
            _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as e:
        print(f"DB Init Error: {e}")
        return None

def fetch_leads():
    db = get_db()
    if not db: return []
    try:
        response = db.table("leads").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Fetch Error: {e}")
        return []

def insert_lead(lead_dict):
    db = get_db()
    if not db: return False
    try:
        db.table("leads").insert(lead_dict).execute()
        return True
    except Exception as e:
        print(f"Insert Error: {e}")
        return False
