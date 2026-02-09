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

# Add Project Root to Path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    from pocket_compliance.dashboard import main
    main()
except ImportError as e:
    st.error(f"Failed to load Compliance: {e}")
except Exception as e:
    st.error(f"Error: {e}")