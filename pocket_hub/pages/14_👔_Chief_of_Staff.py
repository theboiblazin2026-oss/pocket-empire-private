import streamlit as st

# --- SECURITY CHECK ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    import streamlit as st
    st.error("Authentication module missing. Please contact administrator.")
    st.stop()
# ----------------------

import time
import sys
import os
import pandas as pd

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
jarvis_dir = os.path.abspath(os.path.join(current_dir, '../../pocket_jarvis'))
if jarvis_dir not in sys.path:
    sys.path.append(jarvis_dir)

import chief_of_staff as cos
try:
    from pocket_invoices.invoice_manager import create_invoice, get_clients
except ImportError:
    def get_clients(): return []
    def create_invoice(*args, **kwargs): return {}

st.set_page_config(
    page_title="Chief of Staff",
    page_icon="👔",
    layout="wide"
)

st.title("👔 Chief of Staff Command Center")
st.caption("High-level overview and executive control.")

# Auto-refresh logic (optional, manual refresh for now to avoid lag)
if st.button("🔄 Refresh Data"):
    st.rerun()

metrics = cos.get_dashboard_metrics()

# Top Row: Critical Vitals
col1, col2, col3, col4 = st.columns(4)

with col1:
    fin = metrics['finance']
    st.metric("S&P 500", fin.get('sp500', 'N/A'))

with col2:
    fin = metrics['finance']
    st.metric("💰 Total Revenue", fin.get('revenue', '$0.00'))
    st.caption(f"Pending: {fin.get('pending', '$0.00')}")
    
    with st.expander("⚡ Quick Invoice"):
        clients = get_clients()
        client_map = {c['name']: c['id'] for c in clients}
        client_name = st.selectbox("Client", options=list(client_map.keys()) if client_map else ["No Clients"])
        
        desc = st.text_input("Item", "Freight Service")
        amount = st.number_input("Amount ($)", min_value=0.0, step=100.0)
        
        if st.button("Send Invoice", use_container_width=True):
            if client_map:
                c_id = client_map[client_name]
                line_items = [{"description": desc, "quantity": 1, "rate": amount}]
                new_inv = create_invoice(c_id, line_items, notes="Quick Invoice from Chief of Staff")
                st.success(f"Invoice #{new_inv['invoice_number']} Created!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("No Client Selected")

with col3:
    sys_h = metrics['system']
    st.metric("CPU Load", f"{sys_h.get('cpu_percent', 0)}%")
    st.metric("RAM Usage", f"{sys_h.get('ram_percent', 0)}%")

with col4:
    agents = metrics['agents']
    st.metric("Lead Puller", agents.get('lead_puller_status', 'Unknown'))
    st.metric("Leads Found", agents.get('lead_puller_leads', 0))

with col4:
    st.metric("WiFi Status", sys_h.get('wifi_status', 'Unknown'))
    st.metric("Bluetooth", sys_h.get('bt_status', 'Unknown'))

st.divider()

# Command Section
st.subheader("⚡ Executive Actions")

ac1, ac2, ac3, ac4 = st.columns(4)

with ac1:
    if st.button("🛡️ Run Compliance Check", use_container_width=True):
        res = cos.trigger_system_action("run_compliance")
        if res['success']:
            st.toast(res['message'], icon="✅")
        else:
            st.error(res['message'])

with ac2:
    if st.button("🗞️ Generate Briefing", use_container_width=True):
        res = cos.trigger_system_action("generate_briefing")
        if res['success']:
            st.toast(res['message'], icon="✅")
        else:
            st.error(res['message'])
            
with ac3:
    if st.button("🧹 System Cleanup", use_container_width=True):
        with st.spinner("Cleaning..."):
            time.sleep(1)
            res = cos.trigger_system_action("system_cleanup")
            st.toast(res['message'], icon="🧹")

with ac4:
    st.button("🚫 Emergency Stop", type="primary", use_container_width=True, help="Stop all background agents (Not Implemented)")

st.divider()

# Recent Activity Log (Placeholder for now)
st.subheader("📜 System Event Log")
log_data = [
    {"Time": "10:00 AM", "Event": "Briefing Generated", "Status": "Success"},
    {"Time": "09:45 AM", "Event": "Lead Scraper Finished", "Status": "Success (12 Leads)"},
    {"Time": "09:00 AM", "Event": "Compliance Check", "Status": "No Issues"},
]
st.dataframe(pd.DataFrame(log_data), use_container_width=True)