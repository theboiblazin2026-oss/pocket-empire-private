import streamlit as st
import datetime
import time
import os
import sys

# Ensure modules are loaded
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_wealth')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_leads')))

try:
    import wealth_manager as wm
    import search_engine
except ImportError:
    pass

import socket
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

st.set_page_config(
    page_title="Pocket Empire Command Center",
    page_icon="🚀",
    layout="wide"
)

# --- SECURITY CHECK ---
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    st.error("Authentication module missing.")
    st.stop()
# ----------------------

# --- Sidebar Search ---
# --- Sidebar Search ---
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.info(f"📱 **Road Mode**\n Connect: `http://{get_local_ip()}:8501`")

st.sidebar.markdown("### 🔍 Global Search")
search_query = st.sidebar.text_input("Find Lead, Route, Client...", key="global_search_input")

if search_query:
    if 'search_engine' in locals():
        results = search_engine.search_app(search_query)
        if results:
            st.sidebar.success(f"Found {len(results)} matches")
            for idx, res in enumerate(results):
                with st.sidebar.expander(f"{res['Type']}: {res['Name']}"):
                    st.caption(res['Details'])
                    if st.button("Go ➡️", key=f"go_search_{idx}"):
                        st.switch_page(res['Page'])
        else:
            st.sidebar.warning("No matches found.")
    else:
        st.sidebar.error("Search module not loaded.")

st.sidebar.divider()

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
# --- Dashboard Grid ---
# Row 1: Alerts & Wealth
r1_col1, r1_col2 = st.columns(2)

with r1_col1:
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

# --- 2. WEALTH MANAGER ---
with r1_col2:
    try:
        if 'wm' not in locals():
            import wealth_manager as wm
        
        # Load Net Worth
        nw_data = wm.get_latest_net_worth("myself")
        net_worth = nw_data.get("net_worth", 0.0)
        
        # Load Goal Progress (Daily Grind)
        prog = wm.get_daily_progress("myself")
        
        st.subheader("💰 Wealth")
        st.metric("Net Worth", f"${net_worth:,.0f}", delta=f"${prog['earned']:.0f} today")
        
        # Add Credit Score here too as it relates to financial health
        # Load Personal Credit JSON directly for speed
        credit_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_credit/personal_credit.json'))
        if os.path.exists(credit_path):
            import json
            with open(credit_path, 'r') as f:
                c_data = json.load(f)
            
            dispute_count = len(c_data.get("disputes", []))
            
            lbl = f"{dispute_count} Active Disputes"
            st.metric("💳 Credit Repair", "Active", lbl)
        else:
             st.metric("Credit Repair", "Setup", "Mod 02")

    except Exception as e:
        st.metric("Wealth Manager", "Active", "Mod 01")

st.divider()

# Row 2: Actions & Invoices
r2_col1, r2_col2 = st.columns(2)

with r2_col1:
    st.subheader("🧾 Invoices")
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_invoices')))
        import invoice_manager as im
        
        stats = im.get_stats()
        unpaid = stats.get("unpaid_amount", 0.0)
        pending_count = stats.get("unpaid_count", 0)
        
        if pending_count > 0:
            st.metric("Unpaid Invoices", f"${unpaid:,.0f}", delta=f"{pending_count} pending", delta_color="inverse")
        else:
            st.metric("Invoices", "All Paid", "Nice!")
            
    except ImportError:
        val = "Ready" 
        st.metric("Invoice Manager", val, "Mod 13")
    except Exception as e:
        st.metric("Invoice Manager", "Ready", "Mod 13")

with r2_col2:
    st.subheader("⚖️ Legal Assist")
    st.info("Ask legal questions in Pocket Lawyer.")
    if st.button("Open Pocket Lawyer", use_container_width=True):
        st.switch_page("pages/13_⚖️_Pocket_Lawyer.py")

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

st.divider()
if st.button("🎓 Launch Pocket Academy (Curriculum)", use_container_width=True):
    import webbrowser
    webbrowser.open_new_tab("http://localhost:8510")

# --- Footer ---
st.caption(f"System Online | {datetime.datetime.now().strftime('%A, %B %d')} | Pocket Empire Cloud v1.0")
