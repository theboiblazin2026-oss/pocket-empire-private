import streamlit as st
import sys
import os
import importlib

# Add pocket_credit to sys.path
CREDIT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_credit'))
if CREDIT_DIR not in sys.path:
    sys.path.append(CREDIT_DIR)

# Import module with alias to avoid conflict with wealth dashboard if cached?
# sys.modules key is 'dashboard'. 
# This IS A CONFLICT. 
# If 'dashboard' is already imported from pocket_wealth, `import dashboard` will return THAT one.

# SOLUTION: Manually load from file spec to avoid namespace collision.

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# We use valid python module names (no spaces/emojis) for the internal module key
try:
    credit_dashboard = load_module_from_path("credit_dashboard_module", os.path.join(CREDIT_DIR, "dashboard.py"))
    credit_dashboard.main()
except Exception as e:
    st.error(f"Failed to load Credit Dashboard: {e}")
