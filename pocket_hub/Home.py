import streamlit as st
import datetime
import os
import sys

# Ensure modules are loaded
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_wealth')))
try:
    import wealth_manager as wm
except ImportError:
    pass

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
    
    # Dynamic Lead Stats
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_leads')))
        from lead_history import get_lead_stats
        stats = get_lead_stats()
        new_leads = stats.get("New", 0)
        
        if new_leads > 0:
            if st.button(f"ℹ️ Leads: {new_leads} New pending review", type="primary", use_container_width=True):
                st.session_state["lead_filter"] = "New"
                st.switch_page("pages/06_📋_Lead_Pipeline.py")
        else:
            st.info("✅ All leads reviewed")
    except Exception as e:
        st.info("ℹ️ Leads: Check Pipeline")

    # Quick Log Earnings
    with st.expander("⚡ Quick Log Earnings"):
        with st.form("quick_log"):
            q_amt = st.number_input("Amount ($)", min_value=0.0, step=10.0, key="q_amt")
            
            # Try to load streams
            q_sources = ["Gig Work", "Trucking Business", "Other"]
            try:
                if 'wm' in locals():
                    q_data = wm.load_data("myself")
                    loaded_streams = [s['name'] for s in q_data.get('budget', {}).get('income_streams', [])]
                    if loaded_streams:
                        q_sources = loaded_streams
            except:
                pass
                
            q_source = st.selectbox("Source", q_sources, key="q_src")
            
            if st.form_submit_button("💰 Log It"):
                if 'wm' in locals():
                    wm.log_earnings("myself", q_amt, q_source, "Quick Log from Home")
                    st.success(f"Logged ${q_amt}!")
                    time.sleep(1) # Visual feedback
                    st.rerun()
                else:
                    st.error("Wealth Manager module not loaded")

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
    if st.button("⛏️ Launch Prospector"):
        st.switch_page("pages/11_⛏️_Prospector.py")
with c2:
    if st.button("🛣️ Check Routes"):
        st.switch_page("pages/10_🛣️_Route_Planner.py")
with c3:
    if st.button("🧾 Run Payroll"):
        st.switch_page("pages/06_🧾_Invoices.py")
with c4:
    if st.button("📋 Compliance"):
        st.switch_page("pages/04_📋_Compliance.py")

# --- Footer ---
st.caption(f"System Online | {datetime.datetime.now().strftime('%A, %B %d')} | Pocket Empire Cloud v1.0")
