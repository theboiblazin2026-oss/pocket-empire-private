import streamlit as st
import os

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["app_password"]:
            st.session_state["password_correct"] = True
            # del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show input if not verified
    st.text_input(
        "🔑 Security Check", type="password", on_change=password_entered, key="password"
    )
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password Incorrect")
        
    st.error("🔒 App is Locked. Enter Password.")
    return False

def require_auth():
    """Call this at the top of every page to require authentication."""
    if not check_password():
        st.stop()
