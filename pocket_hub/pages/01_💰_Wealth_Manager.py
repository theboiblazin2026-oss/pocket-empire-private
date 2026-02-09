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
WEALTH_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_wealth'))

# Import module safely
def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

try:
    # We must ensure sys.path has WEALTH_DIR so internal imports in dashboard.py (like wealth_manager) work?
    # No, dashboard.py imports `wealth_manager`.
    # If we run dashboard.py via importlib from WEALTH_DIR, does it find wealth_manager?
    # ONLY if WEALTH_DIR is in sys.path.
    if WEALTH_DIR not in sys.path:
        sys.path.append(WEALTH_DIR)

    wealth_dashboard = load_module_from_path("wealth_dashboard_module", os.path.join(WEALTH_DIR, "dashboard.py"))
    wealth_dashboard.main()
except Exception as e:
    st.error(f"Failed to load Wealth Manager: {e}")