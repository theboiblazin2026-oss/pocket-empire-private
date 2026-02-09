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

import sys
import os
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_leads')))

try:
    import lead_history as lh
except ImportError:
    st.error("Could not load lead history module")
    st.stop()

def main():
    try:
        st.set_page_config(
            page_title="📋 Lead Pipeline",
            page_icon="📋",
            layout="wide"
        )
    except:
        pass

    st.title("📋 Lead Pipeline & Follow-ups")
    st.caption("Track every lead, never miss a follow-up")

    # --- Top Stats ---
    stats = lh.get_lead_stats()
    
    # Sync Button (Sidebar)
    with st.sidebar:
        st.header("⚙️ Settings")
        if st.button("🔄 Sync from Prospector"):
            with st.spinner("Syncing leads from Google Sheets..."):
                 # Path to creds (hardcoded based on knowledge)
                 creds_path = "/Volumes/CeeJay SSD/Projects/lead puller/service_account.json"
                 count, msg = lh.sync_from_sheet(creds_path)
                 if count > 0:
                     st.success(msg)
                     st.rerun()
                 else:
                     st.info(msg)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("🔥 Due Today", stats.get("due_today", 0))
    with c2:
        st.metric("📥 New", stats.get("New", 0))
    with c3:
        st.metric("📞 Contacted", stats.get("Contacted", 0))
    with c4:
        st.metric("💰 Won", stats.get("Won", 0))
    with c5:
        st.metric("📊 Total", stats.get("total", 0))

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["🔔 Follow-ups", "📋 Pipeline", "➕ Add Lead", "📊 Analytics"])

    # --- Follow-ups Tab ---
    with tab1:
        st.subheader("🔔 Follow-up Reminders")
        
        # Due Today / Overdue
        due = lh.get_due_follow_ups()
        if due:
            st.error(f"⚠️ {len(due)} follow-up(s) due today or overdue!")
            for lead in due:
                with st.container():
                    c1, c2, c3 = st.columns([2, 1, 1])
                    with c1:
                        st.markdown(f"**{lead.get('company_name', 'Unknown')}**")
                        st.caption(f"📞 {lead.get('phone', 'N/A')} | 📧 {lead.get('email', 'N/A')}")
                    with c2:
                        st.warning(f"Due: {lead.get('follow_up_date', 'N/A')}")
                    with c3:
                        if st.button("✅ Done", key=f"due_{lead['id']}"):
                            lh.add_lead_note(lead['id'], "Follow-up completed", "Call")
                            lh.set_follow_up(lead['id'], None)
                            st.rerun()
                    st.divider()
        else:
            st.success("✅ No overdue follow-ups!")
        
        # Upcoming
        st.markdown("### 📅 Upcoming (Next 7 Days)")
        upcoming = lh.get_upcoming_follow_ups(7)
        if upcoming:
            for lead in upcoming:
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"**{lead.get('company_name', 'Unknown')}** - {lead.get('status', 'New')}")
                    with c2:
                        st.info(f"📅 {lead.get('follow_up_date', 'N/A')}")
        else:
            st.info("No follow-ups scheduled for the next 7 days")

    # --- Pipeline Tab ---
    with tab2:
        st.subheader("📋 Lead Pipeline")
        
        # Filters
        f1, f2 = st.columns(2)
        with f1:
            # Default to "New" if set in session state
            default_ix = 0
            if "lead_filter" in st.session_state and st.session_state["lead_filter"] in ["All"] + lh.LEAD_STATUSES:
                default_ix = (["All"] + lh.LEAD_STATUSES).index(st.session_state["lead_filter"])
                # Clear it after using so it doesn't stick forever
                del st.session_state["lead_filter"]
            
            status_filter = st.selectbox("Filter by Status", ["All"] + lh.LEAD_STATUSES, index=default_ix)
        with f2:
            search = st.text_input("🔍 Search", placeholder="Company or contact name...")
        
        # Get leads
        if search:
            leads = lh.search_leads(search)
        elif status_filter != "All":
            leads = lh.get_leads_by_status(status_filter)
        else:
            leads = lh.load_leads()
        
        st.caption(f"Showing {len(leads)} leads")
        
        # Lead List
        for lead in leads:
            with st.expander(f"{lead.get('company_name', 'Unknown')} | {lead.get('status', 'New')}", expanded=False):
                c1, c2 = st.columns([2, 1])
                
                with c1:
                    st.markdown(f"**MC#:** {lead.get('mc_number', 'N/A')}")
                    st.markdown(f"**Contact:** {lead.get('contact_name', 'N/A')}")
                    st.markdown(f"**Phone:** {lead.get('phone', 'N/A')}")
                    st.markdown(f"**Email:** {lead.get('email', 'N/A')}")
                    st.caption(f"Added: {lead.get('created_at', 'Unknown')[:10]}")
                
                with c2:
                    # Status Update
                    new_status = st.selectbox(
                        "Update Status",
                        lh.LEAD_STATUSES,
                        index=lh.LEAD_STATUSES.index(lead.get('status', 'New')) if lead.get('status') in lh.LEAD_STATUSES else 0,
                        key=f"status_{lead['id']}"
                    )
                    if new_status != lead.get('status'):
                        if st.button("💾 Update", key=f"update_{lead['id']}"):
                            lh.update_lead_status(lead['id'], new_status)
                            st.success("Updated!")
                            st.rerun()
                    
                    # Follow-up
                    st.markdown("---")
                    follow_date = st.date_input("Follow-up Date", key=f"date_{lead['id']}")
                    if st.button("📅 Set Reminder", key=f"remind_{lead['id']}"):
                        lh.set_follow_up(lead['id'], str(follow_date))
                        st.success(f"Reminder set for {follow_date}")
                        st.rerun()
                
                # History
                st.markdown("### 📜 History")
                history = lead.get('history', [])
                if history:
                    for h in reversed(history[-5:]):
                        st.caption(f"**{h.get('date', '')[:10]}** - {h.get('action', '')} - {h.get('notes', '')}")
                else:
                    st.caption("No history yet")
                
                # Add Note
                with st.form(f"note_{lead['id']}"):
                    note = st.text_input("Add Note")
                    action = st.selectbox("Type", ["Note", "Call", "Email", "Meeting"])
                    if st.form_submit_button("➕ Add"):
                        if note:
                            lh.add_lead_note(lead['id'], note, action)
                            st.success("Note added!")
                            st.rerun()

    # --- Add Lead Tab ---
    with tab3:
        st.subheader("➕ Add New Lead")
        
        with st.form("add_lead"):
            company = st.text_input("Company Name *", placeholder="ABC Trucking LLC")
            mc = st.text_input("MC/DOT Number", placeholder="MC123456")
            
            c1, c2 = st.columns(2)
            with c1:
                contact = st.text_input("Contact Name", placeholder="John Smith")
                phone = st.text_input("Phone", placeholder="(555) 123-4567")
            with c2:
                email = st.text_input("Email", placeholder="john@company.com")
                notes = st.text_area("Notes", placeholder="Initial notes about this lead...")
            
            if st.form_submit_button("💾 Add Lead"):
                if company:
                    lh.add_lead(company, mc, contact, phone, email, notes)
                    st.success(f"Added: {company}")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Company name required")

    # --- Analytics Tab ---
    with tab4:
        st.subheader("📊 Pipeline Analytics")
        
        # Status breakdown
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### Pipeline Breakdown")
            pipeline_data = []
            for status in lh.LEAD_STATUSES:
                count = stats.get(status, 0)
                if count > 0:
                    pipeline_data.append({"Status": status, "Count": count})
            
            if pipeline_data:
                df = pd.DataFrame(pipeline_data)
                st.bar_chart(df.set_index("Status"))
            else:
                st.info("Add leads to see analytics")
        
        with c2:
            st.markdown("### Quick Stats")
            total = stats.get("total", 0)
            if total > 0:
                won = stats.get("Won", 0)
                lost = stats.get("Lost", 0)
                
                st.metric("Win Rate", f"{(won/total*100):.1f}%" if total > 0 else "0%")
                st.metric("Conversion", f"{won}/{total} leads won")
                st.metric("Active Pipeline", total - won - lost)
            else:
                st.info("No data yet")

if __name__ == "__main__":
    main()