
import streamlit as st
import sys
import os

st.title("🚧 DEBUG MODE 🚧")
st.write("If you see this, Streamlit works!")
st.write(f"Python: {sys.version}")
st.write(f"Current Dir: {os.getcwd()}")
st.write(f"Files here: {os.listdir('.')}")

try:
    st.write("Testing Imports...")
    import supabase
    st.success("Supabase imported")
    import pandas
    st.success("Pandas imported")
except Exception as e:
    st.error(f"Import failed: {e}")

st.write("Testing System Path...")
st.code(str(sys.path))
