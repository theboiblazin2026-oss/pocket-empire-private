import streamlit as st
import os

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # TARGET_SECRET_NAME = "app_password"
        if "app_password" not in st.secrets:
            st.error("🚨 System Error: 'app_password' not found in secrets. Please update Streamlit Cloud settings.")
            return

        if st.session_state.get("password") == st.secrets["app_password"]:
            st.session_state["password_correct"] = True
            # Optional: Clear the password from text input to be cleaner
            # st.session_state["password"] = "" 
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show input if not verified
    st.text_input(
        "🔑 Security Check", type="password", on_change=password_entered, key="password"
    )
    
    # Check for missing secret upfront to prevent crash
    if "app_password" not in st.secrets:
        st.error("⚠️ Admin: Please add 'app_password' to your .streamlit/secrets.toml or Cloud Secrets.")
        return False
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password Incorrect")
        
    st.warning("🔒 App is Locked. Enter Password.")
    return False

def require_auth():
    """Call this at the top of every page to require authentication."""
    if not check_password():
        st.stop()
