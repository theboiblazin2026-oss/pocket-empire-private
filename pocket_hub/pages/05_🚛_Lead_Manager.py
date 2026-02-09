import streamlit as st
import sys
import os

# Add Project Root to Path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    from pocket_leads.dashboard import main
    main()
except ImportError as e:
    st.error(f"Failed to load Lead Manager: {e}")
except Exception as e:
    st.error(f"Error: {e}")
