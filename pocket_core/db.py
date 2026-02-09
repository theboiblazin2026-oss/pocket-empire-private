import streamlit as st
from supabase import create_client, Client
import os

# Singleton pattern for DB connection
_supabase_client = None

def reset_db():
    """Force re-initialization of the DB client (e.g. after settings change)."""
    global _supabase_client
    _supabase_client = None

def get_db():
    global _supabase_client
    
    url = None
    key = None

    # 1. Try Session State (Immediate Update)
    if "SUPABASE_URL" in st.session_state:
        url = st.session_state["SUPABASE_URL"]
    if "SUPABASE_KEY" in st.session_state:
        key = st.session_state["SUPABASE_KEY"]
    
    # 2. Try Secrets (Cloud)
    if not url:
        try:
            url = st.secrets.get("SUPABASE_URL")
        except Exception: pass
    if not key:
        try:
            key = st.secrets.get("SUPABASE_KEY")
        except Exception: pass
    
    # 3. Fallback to Env (Local)
    if not url: url = os.getenv("SUPABASE_URL")
    if not key: key = os.getenv("SUPABASE_KEY")
    
    # 3b. Fallback to Manual TOML Load (for CLI scripts)
    if not url or not key:
        try:
            import toml
            # Calculate path relative to pocket_core/db.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            secrets_path = os.path.abspath(os.path.join(current_dir, '..', '.streamlit', 'secrets.toml'))
            
            if os.path.exists(secrets_path):
                data = toml.load(secrets_path)
                if not url: url = data.get("SUPABASE_URL")
                if not key: key = data.get("SUPABASE_KEY")
        except Exception:
            pass

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

# --- Notes ---
def fetch_notes(user_id=None):
    db = get_db()
    if not db: return []
    try:
        # If user_id is provided, filter by it. For now, fetch all or implement simple RLS.
        # Assuming RLS handles user filtering if Auth is on.
        # Otherwise, we might want to filter by a 'demo_user' ID if we don't have real auth yet.
        response = db.table("notes").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Fetch Notes Error: {e}")
        return []

def save_note_db(note_data):
    """
    note_data: {title, content, drawing_data, user_id (optional)}
    """
    db = get_db()
    if not db: return False
    try:
        db.table("notes").insert(note_data).execute()
        return True
    except Exception as e:
        print(f"Save Note Error: {e}")
        return False

def delete_note_db(note_id):
    db = get_db()
    if not db: return False
    try:
        db.table("notes").delete().eq("id", note_id).execute()
        return True
    except Exception as e:
        print(f"Delete Note Error: {e}")
        return False

# --- Inspections ---
def fetch_inspections():
    db = get_db()
    if not db: return []
    try:
        response = db.table("inspections").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Fetch Inspections Error: {e}")
        return []

def save_inspection_db(inspection_data):
    """
    inspection_data: Dictionary containing full BOL data (shipper, carrier, cargo, images, etc.)
    """
    db = get_db()
    if not db: return False
    try:
        # Extract title if present, otherwise default
        title = inspection_data.get("title", f"Inspection {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Payload for Supabase
        payload = {
            "title": title,
            "data": inspection_data,  # Store full object in JSONB column
            "created_at": "now()"
        }
        
        db.table("inspections").insert(payload).execute()
        return True
    except Exception as e:
        print(f"Save Inspection Error: {e}")
        return False
