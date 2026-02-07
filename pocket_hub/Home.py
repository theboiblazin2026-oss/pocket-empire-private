import streamlit as st
import datetime
import os

st.set_page_config(
    page_title="Pocket Empire Command Center",
    page_icon="🚀",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .big-font { font-size: 20px !important; }
    .stMetric {
        background-color: #1E2129;
        border: 1px solid #333;
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
BANNER_PATH = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(BANNER_PATH):
    st.image(BANNER_PATH, width=700)
else:
    st.title("🚀 Pocket Empire Command Center")

# --- Dashboard Grid ---
col_alerts, col_wealth, col_credit, col_law = st.columns([2, 1, 1, 1])

with col_alerts:
    st.subheader("🚨 Alerts")
    
    # Check if Supabase is configured
    try:
        supabase_url = st.secrets.get("SUPABASE_URL", None)
        if supabase_url:
            st.success("✅ Database: **Connected**")
        else:
            st.warning("⚠️ Database: **Offline** (Add Keys to Secrets)")
    except Exception:
        st.warning("⚠️ Database: **Offline** (Add Keys to Secrets)")
    
    st.info("ℹ️ Leads: **5 New** pending review")

with col_wealth:
    st.metric("Wealth Manager", "Active", "Mod 01")

with col_credit:
    st.metric("Credit Repair", "Active", "Mod 02")

with col_law:
    st.metric("Pocket Lawyer", "Ready", "Mod 13")

# --- Quick Actions Row ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.button("⛏️ Launch Prospector")
with c2:
    st.button("🛣️ Check Routes")
with c3:
    st.button("🧾 Run Payroll")
with c4:
    st.button("📋 Compliance")

# --- Footer ---
st.caption(f"System Online | {datetime.datetime.now().strftime('%A, %B %d')} | Pocket Empire Cloud v1.0")
