import streamlit as st
import datetime
import os
import json

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
BANNER_PATH = "/Users/newguy/.gemini/antigravity/brain/7ee22e88-9edf-4e14-b473-1bce1477c2f5/pocket_empire_logo_ultra_cropped.png"
if os.path.exists(BANNER_PATH):
    st.image(BANNER_PATH, use_container_width=True)

# --- Dashboard Grid ---
# Row 1: Alerts (Left) + Critical Stats (Right)
col_alerts, col_wealth, col_credit, col_law = st.columns([2, 1, 1, 1])

with col_alerts:
    st.subheader("🚨 Alerts")
    alerts_found = False
    
    # 0. Database Status
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
        import db
        if db.get_db():
            st.success("✅ Database: **Connected**")
        else:
            st.warning("⚠️ Database: **Offline** (Add Keys to Secrets)")
            alerts_found = True
    except Exception as e:
        st.error(f"DB Error: {e}")
    
    # 1. Credit Check
    try:
        with open("/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_credit/personal_credit.json") as f:
            credit_data = json.load(f)
            score = credit_data.get("current_score", 0)
            if score < 700:
                st.error(f"⚠️ Credit Score: **{score}** (Goal: 750+)")
                alerts_found = True
    except:
        pass

    # 2. Lead Check (Mock)
    st.info("ℹ️ Leads: **5 New** pending review")
    
    if not alerts_found:
        st.caption("No critical system failures.")

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
    st.button("⛏️ Launch Prospector", use_container_width=True)
with c2:
    st.button("🛣️ Check Routes", use_container_width=True)
with c3:
    st.button("🧾 Run Payroll", use_container_width=True)
with c4:
    st.button("📋 Compliance", use_container_width=True)

# --- Footer ---
st.caption(f"System Online | {datetime.datetime.now().strftime('%A, %B %d')} | Theme: Dark Gold")
