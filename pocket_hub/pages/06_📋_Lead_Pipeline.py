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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path for imports
# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_leads')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_invoices')))

try:
    import lead_history as lh
    import ai_analyst
    import invoice_manager as im
except ImportError:
    st.error("Could not load lead modules")
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
        
        # --- SMART AUTO-SYNC ---
        # Initialize last sync time if not present
        if 'last_sync_time' not in st.session_state:
            st.session_state['last_sync_time'] = None

        def run_sync(silent=False):
            """Core logic to sync 'Replied' leads from both bots"""
            new_leads_found = False
            msg = ""
            
            # 1. Sync Web Hunter
            web_creds = "/Volumes/CeeJay SSD/Projects/lead puller/service_account.json"
            web_added, web_msg = lh.sync_from_sheet(web_creds)
            
            # 2. Sync Fleet Manager
            fleet_creds = "/Volumes/CeeJay SSD/Truck Scraper Master File/service_account.json"
            fleet_id = "1Z-P_f8M... (Load from secrets in real app)" 
            
            fleet_added = []
            try:
                import toml
                # Try to load secrets
                secrets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".streamlit", "secrets.toml")
                if os.path.exists(secrets_path):
                    secs = toml.load(secrets_path)
                    if "fleet_manager" in secs:
                        fleet_id = secs["fleet_manager"]["sheet_id"]
                        fleet_added, fleet_msg = lh.sync_fleet_manager(fleet_creds, fleet_id)
            except:
               pass

            total_new = 0
            # Safety check: Ensure lists are actually lists
            if isinstance(web_added, list):
                total_new += len(web_added)
            if isinstance(fleet_added, list):
                total_new += len(fleet_added)
            
            # --- AI ANALYSIS ---
            if total_new > 0:
                with st.spinner("🧠 AI Analyzing Replies..."):
                    # 1. Analyze Web Leads
                    if isinstance(web_added, list) and web_added:
                        # Get Creds
                        w_user = ""
                        w_pass = ""
                        if "web_hunter" in st.secrets:
                            w_user = st.secrets["web_hunter"].get("mailer_email", "")
                            w_pass = st.secrets["web_hunter"].get("mailer_password", "")
                        
                        if w_user and w_pass:
                            for l in web_added:
                                body = ai_analyst.fetch_latest_email(l['email'], "imap.gmail.com", w_user, w_pass)
                                if body:
                                    analysis = ai_analyst.analyze_reply(body)
                                    if "error" not in analysis:
                                        # Auto-Update
                                        lh.update_lead_status(l['id'], analysis.get("suggested_status", "New"))
                                        lh.add_lead_note(l['id'], f"AI Analysis: {analysis.get('summary')}\nSentiment: {analysis.get('sentiment')}\nIntent: {analysis.get('intent')}")
                                
                    # 2. Analyze Fleet Leads
                    if isinstance(fleet_added, list) and fleet_added:
                        # Get Creds
                        f_user = ""
                        f_pass = ""
                        if "fleet_manager" in st.secrets:
                            f_user = st.secrets["fleet_manager"].get("gmail_username", "")
                            f_pass = st.secrets["fleet_manager"].get("gmail_app_password", "")
                        
                        if f_user and f_pass:
                            for l in fleet_added:
                                body = ai_analyst.fetch_latest_email(l['email'], "imap.gmail.com", f_user, f_pass)
                                if body:
                                    analysis = ai_analyst.analyze_reply(body)
                                    if "error" not in analysis:
                                        # Auto-Update
                                        lh.update_lead_status(l['id'], analysis.get("suggested_status", "New"))
                                        lh.add_lead_note(l['id'], f"AI Analysis: {analysis.get('summary')}\nSentiment: {analysis.get('sentiment')}\nIntent: {analysis.get('intent')}")

            if total_new > 0:
                new_leads_found = True
                msg = f"🎉 Found {total_new} New Replies!\n\n"
                if isinstance(web_added, list) and web_added:
                    msg += "**Web Hunter:**\n" + "\n".join([f"- {l['company_name']}: {l['email']}" for l in web_added]) + "\n\n"
                if isinstance(fleet_added, list) and fleet_added:
                    msg += "**Fleet Manager:**\n" + "\n".join([f"- {l['company_name']}: {l['email']}" for l in fleet_added])
                
                # Update Alert
                st.session_state['sync_alert'] = msg
                if not silent:
                    st.balloons()
            elif not silent:
                st.info("No new replies found.")
                
            # Update Timestamp
            st.session_state['last_sync_time'] = datetime.now()
            return new_leads_found

        # Button for Manual Sync
        if st.button("🔄 Sync Replies"):
            with st.spinner("Checking for new replies..."):
                 run_sync(silent=False)
                 st.success("Sync Complete!")

        # Auto-Run Logic (Every 4 Hours)
        now = datetime.now()
        last_run = st.session_state['last_sync_time']
        
        if last_run is None or (now - last_run).total_seconds() > 14400: # 14400 seconds = 4 hours
            with st.spinner("⏳ Auto-Syncing Replies..."):
                run_sync(silent=True)
        
        # Display Last Sync Time
        if last_run:
            st.caption(f"Last checked: {last_run.strftime('%I:%M %p')}")
        else:
            st.caption("Last checked: Just now")
        
        st.divider()
        st.subheader("📄 Info Packet")
        uploaded_file = st.file_uploader("Upload Brochure (PDF)", type="pdf")
        
        BROCHURE_PATH = os.path.join(os.path.dirname(__file__), "../../pocket_leads/data/brochure.pdf")
        if uploaded_file:
            with open(BROCHURE_PATH, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Brochure Saved!")
            
        elif os.path.exists(BROCHURE_PATH):
            st.caption("✅ Brochure loaded and ready to send.")

        # Mobile Toggle
        st.session_state['mobile_view'] = st.toggle("📱 Mobile View", value=st.session_state.get('mobile_view', False))

    # --- METRICS ---
    if st.session_state.get('mobile_view'):
        # 3x2 Grid for Mobile
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("🔥 Due", stats.get("due_today", 0))
        with m2: st.metric("📥 New", stats.get("New", 0))
        with m3: st.metric("📞 Contacted", stats.get("Contacted", 0))
        
        m4, m5, m6 = st.columns(3)
        with m4: st.metric("💰 Won", stats.get("Won", 0))
        with m5: st.metric("📊 Total", stats.get("total", 0))
        with m6: st.metric("💵 Value", f"${stats.get('pipeline_value', 0):,.0f}")
    else:
        # --- VISUAL ANALYTICS (Plotly) ---
        c1, c2 = st.columns(2)
        with c1:
            # Revenue Forecast (Deal Value by Status)
            try:
                leads = lh.load_leads()
                df = pd.DataFrame(leads)
                if not df.empty and "deal_value" in df.columns:

                     df["deal_value"] = pd.to_numeric(df["deal_value"], errors='coerce').fillna(0)
                     rev = df.groupby("status")["deal_value"].sum().reset_index()
                     
                     fig = px.bar(rev, x="status", y="deal_value", title="💰 Revenue Forecast by Stage", 
                                  color="status", color_discrete_sequence=px.colors.qualitative.Pastel)
                     fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20), showlegend=False)
                     st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Add deal values to see revenue forecast")
            except:
                st.info("Chart unavailable")
        
        with c2:
            # Pipeline Funnel
            try:
                funnel_data = {"Stage": [], "Count": []}
                for s in ["New", "Contacted", "Proposal", "Negotiation", "Won"]:
                    count = stats.get(s, 0)
                    if count > 0:
                        funnel_data["Stage"].append(s)
                        funnel_data["Count"].append(count)
                
                if funnel_data["Stage"]:
                    fig = px.funnel(funnel_data, x='Count', y='Stage', title="🔻 Sales Funnel")
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Pipeline empty")
            except:
                pass
    
    # Original Metrics Row (Compact)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("🔥 Due Today", stats.get("due_today", 0))
    with c2: st.metric("📥 New Leads", stats.get("New", 0))
    with c3: st.metric("💰 Won Deals", stats.get("Won", 0))
    with c4: st.metric("💵 Pipeline Value", f"${stats.get('pipeline_value', 0):,.0f}")


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
            val_str = f"${lead.get('deal_value', 0):,.0f}" if lead.get('deal_value') else "$0"
            with st.expander(f"{lead.get('company_name', 'Unknown')} | {lead.get('status', 'New')} | {val_str}", expanded=False):
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
                        if st.button("💾 Update Status", key=f"update_{lead['id']}"):
                            lh.update_lead_status(lead['id'], new_status)
                            st.success("Updated!")
                            st.success("Updated!")
                            st.rerun()

                    # Convert to Client (If Won)
                    if lead.get('status') == "Won":
                        if st.button("🎉 Convert to Client", key=f"conv_{lead['id']}"):
                            try:
                                im.add_client(
                                    name=lead.get('company_name', 'Unknown'),
                                    address="Address Pending", 
                                    city_state_zip="",
                                    email=lead.get('email', ''),
                                    phone=lead.get('phone', '')
                                )
                                st.success(f"Client Profile Created for {lead.get('company_name')}!")
                                st.balloons()
                                lh.add_lead_note(lead['id'], "Converted to Client", "System")
                            except Exception as e:
                                st.error(f"Conversion Failed: {e}")
                    
                    # Edit Value
                    curr_val = float(lead.get('deal_value', 0.0))
                    new_val = st.number_input("Deal Value ($)", value=curr_val, step=100.0, key=f"val_{lead['id']}")
                    if new_val != curr_val:
                         if st.button("💾 Save Value", key=f"save_val_{lead['id']}"):
                             lh.update_lead(lead['id'], deal_value=new_val)
                             st.success("Value Saved!")
                             st.rerun()
                    
                    # Send Brochure
                    if os.path.exists(BROCHURE_PATH):
                        if st.button("📤 Send Brochure", key=f"send_broch_{lead['id']}"):
                            # 1. Get Mailer Config
                            m_user = ""
                            m_pass = ""
                            if "web_hunter" in st.secrets:
                                m_user = st.secrets["web_hunter"].get("mailer_email", "")
                                m_pass = st.secrets["web_hunter"].get("mailer_password", "")
                            
                            if m_user and m_pass:
                                try:
                                    msg = MIMEMultipart()
                                    msg['From'] = m_user
                                    msg['To'] = lead['email']
                                    msg['Subject'] = f"Info for {lead['company_name']} - Pocket Empire" # Basic subject
                                    
                                    body = "Hi,\n\nHere is the information you requested.\n\nBest,\nSales Team"
                                    msg.attach(MIMEText(body, 'plain'))
                                    
                                    with open(BROCHURE_PATH, "rb") as f:
                                        part = MIMEApplication(f.read(), Name="Brochure.pdf")
                                    part['Content-Disposition'] = 'attachment; filename="Brochure.pdf"'
                                    msg.attach(part)
                                    
                                    s = smtplib.SMTP('smtp.gmail.com', 587)
                                    s.starttls()
                                    s.login(m_user, m_pass)
                                    s.sendmail(m_user, lead['email'], msg.as_string())
                                    s.quit()
                                    
                                    st.success("Brochure Sent!")
                                    lh.add_lead_note(lead['id'], "Sent Brochure", "Email")
                                    lh.update_lead_status(lead['id'], "Contacted")
                                except Exception as e:
                                    st.error(f"Send Failed: {e}")
                            else:
                                st.error("Mailer Config Missing in Secrets")


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
                deal_val = st.number_input("Est. Deal Value ($)", min_value=0.0, step=100.0)
                notes = st.text_area("Notes", placeholder="Initial notes about this lead...")
            
            if st.form_submit_button("💾 Add Lead"):
                if company:
                    lh.add_lead(company, mc, contact, phone, email, notes, deal_value=deal_val)
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