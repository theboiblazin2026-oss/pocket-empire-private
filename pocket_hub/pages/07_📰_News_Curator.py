import streamlit as st
import sys
import os
import importlib.util

DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_news'))

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

try:
    if DIR not in sys.path:
        sys.path.append(DIR)
    
    mod = load_module("news_dash_mod", os.path.join(DIR, "dashboard.py"))
    mod.main()
except Exception as e:
    st.error(f"Failed to load News: {e}")
