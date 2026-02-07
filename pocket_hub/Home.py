
import streamlit as st
import sys
import os

st.set_page_config(page_title="Debug Mode", page_icon="🐛")

st.title("✅ HELLO WORLD")
st.write("If you see this, the app is running!")

st.header("System Info")
st.write(f"Python Version: `{sys.version}`")
st.write(f"Working Dir: `{os.getcwd()}`")

st.header("Dependency Check")
libs = ["pandas", "numpy", "supabase", "folium", "plotly"]
for lib in libs:
    try:
        __import__(lib)
        st.success(f"✅ {lib} loaded")
    except ImportError as e:
        st.error(f"❌ {lib} failed: {e}")
    except Exception as e:
        st.error(f"⚠️ {lib} crashed: {e}")

st.button("Click me to verify interactivity")
