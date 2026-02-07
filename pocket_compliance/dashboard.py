import streamlit as st
import pandas as pd
import json
import os
import sys

# Ensure tools can be found
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from tools.monitor import get_carrier_status, get_monitored_mcs, add_mc, remove_mc

# Paths
HISTORY_FILE = os.path.join(DIR, "history.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, 'r') as f:
        return json.load(f)

def main():
    # Page Config (Guarded)
    try:
        st.set_page_config(
            page_title="🛡️ Compliance Officer",
            page_icon="🛡️",
            layout="wide"
        )
    except:
        pass

    # Sidebar
    st.sidebar.title("🛡️ Compliance Officer")
    st.sidebar.markdown("Automated FMCSA Monitoring")

    # Action: Add Client
    st.sidebar.header("Add Client")
    
    with st.sidebar.expander("➕ Add New Carrier"):
        col1, col2 = st.columns([2, 2])
        with col1:
            new_mc = st.text_input("Enter MC/DOT Number", placeholder="e.g. MC:12345")
        with col2:
            new_alias = st.text_input("Company Name", placeholder="My Trucking Co")
            
        if st.button("Track Carrier"):
            if new_mc:
                if add_mc(new_mc, new_alias):
                    st.success(f"Added {new_mc}")
                    st.rerun()
                else:
                    st.warning("Already tracking.")
            else:
                st.error("Enter ID.")

    # Display tracked carriers
    mcs_data = get_monitored_mcs()

    if not mcs_data:
        st.sidebar.info("No carriers being tracked.")
    else:
        st.sidebar.subheader("Currently Tracking")
        for entry in mcs_data:
            identifier = entry['id']
            alias = entry['alias']
            header_text = f"🚛 {alias} ({identifier})" if alias else f"🚛 {identifier}"
            
            with st.sidebar.expander(header_text):
                if st.button(f"Check Status", key=f"chk_{identifier}"):
                    # Parse ID
                    parts = identifier.split(':')
                    s_type = "USDOT" if parts[0].upper() == "DOT" else "MC_MX"
                    id_val = parts[1] if len(parts)>1 else identifier
                    
                    with st.spinner("Checking..."):
                        data = get_carrier_status(id_val, s_type)
                    st.write(f"Status: {data.get('status', 'Unknown')}")
                
                if st.button("Unsubscribe", key=f"del_{identifier}"):
                    remove_mc(entry['raw'])
                    st.rerun()

    # Main Area
    st.title("Client Overview")
    st.metric("Total Clients", len(mcs_data))

    history = load_history()
    table_data = []

    for entry in mcs_data:
        ident = entry['id']
        # Try to find history
        # We search history values to find matching ID? 
        # Or assumes history keys match 'id' or 'raw'?
        # The history file keyed by '12345' (legacy).
        # We'll key by 'id' in future.
        
        # Simple lookup
        data = history.get(ident, {}) 
        if not data and ':' in ident:
             data = history.get(ident.split(':')[1], {})

        table_data.append({
            "ID": ident,
            "Alias": entry['alias'],
            "Status": data.get("status", "Unknown"),
            "Rating": data.get("rating", "None")
        })

    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)
    
    # Force Run
    if st.button("🔄 Force Refresh All"):
        progress = st.progress(0)
        for i, entry in enumerate(mcs_data):
            ident = entry['id']
            parts = ident.split(':')
            s_type = "USDOT" if parts[0].upper() == "DOT" else "MC_MX"
            id_val = parts[1] if len(parts)>1 else ident
            
            res = get_carrier_status(id_val, s_type)
            history[ident] = res
            progress.progress((i+1)/len(mcs_data))
            
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        st.success("Updated.")
        st.rerun()

if __name__ == "__main__":
    main()
