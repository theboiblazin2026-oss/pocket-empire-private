import streamlit as st
import pandas as pd
import json
import os
import sys

# Ensure tools can be found
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

TOOLS_DIR = os.path.join(DIR, "tools")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)

from vault_manager import save_document, list_documents, get_document_path
from monitor import get_monitored_mcs, add_mc, remove_mc, get_carrier_status

# History file for caching status data
HISTORY_FILE = os.path.join(DIR, "history.json")

def load_history():
    """Load cached carrier status history."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

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

    # Main Tabs
    tab1, tab2 = st.tabs(["🛡️ Client Overview", "📂 Audit Vault"])

    with tab1:
        st.title("Client Overview")
        st.metric("Total Clients", len(mcs_data))

        history = load_history()
        table_data = []

        for entry in mcs_data:
            ident = entry['id']
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

    with tab2:
        st.title("📂 Audit Vault")
        st.caption("Secure document storage for carrier compliance files.")
        
        if not mcs_data:
            st.warning("No carriers found. Add a carrier in the sidebar to start.")
        else:
            # Select Carrier
            options = [f"{e['alias']} ({e['id']})" if e['alias'] else e['id'] for e in mcs_data]
            selected_option = st.selectbox("Select Carrier", options)
            
            # Extract ID
            # Option format: "Alias (ID)" or "ID"
            if "(" in selected_option:
                selected_id = selected_option.split("(")[-1].strip(")")
            else:
                selected_id = selected_option
                
            st.divider()
            
            c1, c2 = st.columns([1, 1])
            
            with c1:
                st.subheader("📤 Upload Document")
                doc_type = st.selectbox("Document Type", ["Insurance", "Authority", "W9", "Contract", "CDL", "Other"])
                uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg", "docx"])
                
                # Expiry Date Input
                has_expiry = st.checkbox("Has Expiration Date?", value=True)
                expiry_date = None
                if has_expiry:
                    expiry_date = st.date_input("Expiration Date")
                
                if uploaded_file and st.button("Save to Vault"):
                    # Convert date to datetime for backend if needed, or pass as date object
                    # proper way is usually datetime.combine
                    expiry_dt = None
                    if expiry_date:
                        import datetime as dt
                        expiry_dt = dt.datetime.combine(expiry_date, dt.datetime.min.time())
                        
                    path = save_document(selected_id, uploaded_file, doc_type, expiry_date=expiry_dt)
                    st.success(f"Saved: {os.path.basename(path)}")
                    st.rerun()
            
            with c2:
                st.subheader("🗄️ Stored Documents")
                docs = list_documents(selected_id)
                
                if not docs:
                    st.info("No documents found for this carrier.")
                else:
                    for doc in docs:
                        label = f"{doc['type']} - {doc['name']}"
                        
                        # Expiry Warning
                        expiry_str = doc.get('expiry_date')
                        status_icon = "🟢"
                        if expiry_str:
                             from datetime import datetime
                             exp = datetime.fromisoformat(expiry_str)
                             days = (exp - datetime.now()).days
                             if days < 0:
                                 status_icon = "🔴"
                                 label += f" (EXPIRED {abs(days)}d ago)"
                             elif days < 30:
                                 status_icon = "🟠"
                                 label += f" (Exp: {days}d)"
                             else:
                                 label += f" (Exp: {exp.strftime('%Y-%m-%d')})"
                        
                        with st.expander(f"{status_icon} {label}"):
                            st.caption(f"📅 Uploaded: {doc['uploaded_at']} | 💾 {doc['size_kb']} KB")
                            st.code(doc['path']) # Show path since we can't easily serve local files without a static server in plain Streamlit
                            
                            if doc['filename'].endswith(('.png', '.jpg', '.jpeg')):
                                st.image(doc['path'])

if __name__ == "__main__":
    main()
