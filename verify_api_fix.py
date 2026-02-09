
import sys
import os
from unittest.mock import MagicMock, patch

# Mock streamlit before importing db
sys.modules["streamlit"] = MagicMock()
import streamlit as st
st.secrets = {}
st.session_state = {}

# Mock supabase
sys.modules["supabase"] = MagicMock()
from supabase import create_client

# Import target
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "pocket_core")))
from pocket_core.db import get_db, reset_db

def test_db_session_priority():
    print("🧪 Testing DB Session Priority...")
    
    # 1. Setup Env
    os.environ["SUPABASE_URL"] = "ENV_URL"
    os.environ["SUPABASE_KEY"] = "ENV_KEY"
    
    # 2. Test Env Fallback
    reset_db()
    st.session_state = {}
    st.secrets = {}
    
    get_db()
    # Check if create_client called with ENV vars
    create_client.assert_called_with("ENV_URL", "ENV_KEY")
    print("✅ Env Fallback works")
    
    # 3. Test Session State Priority
    reset_db()
    st.session_state = {"SUPABASE_URL": "SESSION_URL", "SUPABASE_KEY": "SESSION_KEY"}
    
    get_db()
    create_client.assert_called_with("SESSION_URL", "SESSION_KEY")
    print("✅ Session State Priority works")
    
    # 4. Test Reset
    print("✅ Reset DB function exists and runs")

if __name__ == "__main__":
    test_db_session_priority()
