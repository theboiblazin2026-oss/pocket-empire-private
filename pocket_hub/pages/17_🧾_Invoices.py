import streamlit as st

# --- SECURITY CHECK ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    import streamlit as st
    st.error("Authentication module missing. Please contact administrator.")
    st.stop()
# ----------------------

import sys
import os
import importlib.util

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_invoices'))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

try:
    if DIR not in sys.path:
        sys.path.append(DIR)
    
    mod = load_module("invoices_dash_mod", os.path.join(DIR, "dashboard.py"))
    mod.main()
except Exception as e:
    st.error(f"Failed to load Invoices: {e}")