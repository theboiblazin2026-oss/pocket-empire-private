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

# Paths
SNIPER_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_sniper'))

# Import module safely
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

try:
    if SNIPER_DIR not in sys.path:
        sys.path.append(SNIPER_DIR)

    sniper_dash = load_module_from_path("sniper_dashboard_module", os.path.join(SNIPER_DIR, "sniper_dashboard.py"))
    sniper_dash.main()
except Exception as e:
    st.error(f"Failed to load Deal Finder: {e}")