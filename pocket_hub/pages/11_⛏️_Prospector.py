import streamlit as st
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

import gspread
from google.oauth2.service_account import Credentials
import smtplib
import json
import time
import random
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import streamlit.components.v1 as components

# --- AUTH ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    pass

# --- Page Config ---
try:
    st.set_page_config(page_title="The Prospector", page_icon="⛏️", layout="wide")
except:
    pass

st.title("⛏️ The Prospector")
st.caption("Lead Puller Command Center")

# ==========================================
# CLOUD-READY CREDENTIAL LOADING
# ==========================================
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

# --- LOCAL PATHS (Fallback) ---
LEAD_PULLER_DIR = "/Volumes/CeeJay SSD/Projects/lead puller"
TRUCK_SCRAPER_DIR = "/Volumes/CeeJay SSD/Truck Scraper Master File"
IS_LOCAL = os.path.exists(LEAD_PULLER_DIR)

# --- Default Templates (Embedded for Cloud) ---
DEFAULT_WEB_TEMPLATES = {
  "standard": {
    "subject_a": "Question about {business_name}",
    "subject_b": "Are you accepting new jobs in {city}?",
    "body": "Hi,\n\nAre you looking to grow your customer base in {city}?\n\nI have a system that brings in consistent jobs for {business_name}, and I'm looking for one partner in the area to work with.\n\nOpen to a quick chat?\n\nBest,\nCalvin Manning\nTech Trap Solutions\n\"Helping you build your customer base with a web trap to catch their attention\""
  },
  "broken_link": {
    "subject": "Question about {business_name}",
    "body": "Hi,\n\nI tried to visit your website earlier but got a \"Page Not Found\" error.\n\nI think you might be losing customers who click on your maps listing.\n\nI fix broken links for local businesses. Want me to get it back online for you tomorrow?\n\nBest,\nCalvin Manning\nTech Trap Solutions\n\"Helping you build your customer base with a web trap to catch their attention\""
  },
  "not_secure": {
    "subject": "Question about {business_name}",
    "body": "Hi,\n\nApplying for a job in the area and noticed your website says \"Not Secure\" when I visit.\n\nGoogle is flagging it, which scares away customers.\n\nI can fix the SSL certificate for you this week if you want?\n\nLet me know,\nCalvin Manning\nTech Trap Solutions\n\"Helping you build your customer base with a web trap to catch their attention\""
  }
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

@st.cache_resource(ttl=300)
def get_web_client():
    """Connect to Web Hunter Google Sheet (credentials from secrets or local file)."""
    try:
        if "web_hunter" in st.secrets and "gcp_service_account" in st.secrets["web_hunter"]:
            creds_dict = dict(st.secrets["web_hunter"]["gcp_service_account"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        elif IS_LOCAL:
            creds_file = os.path.join(LEAD_PULLER_DIR, "service_account.json")
            creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
        else:
            return None
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Web Auth Error: {e}")
        return None

@st.cache_resource(ttl=300)
def get_fleet_client():
    """Connect to Fleet Manager Google Sheet (using its own service account)."""
    try:
        if "fleet_manager" in st.secrets and "gcp_service_account" in st.secrets["fleet_manager"]:
            creds_dict = dict(st.secrets["fleet_manager"]["gcp_service_account"])
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        elif IS_LOCAL:
            creds_file = os.path.join(TRUCK_SCRAPER_DIR, "service_account.json")
            creds = Credentials.from_service_account_file(creds_file, scopes=SCOPES)
        else:
            return None
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Fleet Auth Error: {e}")
        return None

def get_fleet_sheet_id():
    """Get Fleet Sheet ID from secrets or local .env."""
    if "fleet_manager" in st.secrets:
        return st.secrets["fleet_manager"]["sheet_id"]
    elif IS_LOCAL:
        env_path = os.path.join(TRUCK_SCRAPER_DIR, ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("GOOGLE_SHEET_ID="):
                        return line.strip().split("=", 1)[1]
    return None

def get_web_sheet_id():
    """Get Web Hunter Sheet ID from secrets or local config."""
    if "web_hunter" in st.secrets:
        return st.secrets["web_hunter"].get("sheet_id") # Safe get
    return None

def get_web_sheet_name():
    """Get Web Hunter Sheet Name from secrets or default."""
    if "web_hunter" in st.secrets:
        return st.secrets["web_hunter"].get("sheet_name", "Lead Puller Master List")
    return "Lead Puller Master List"

def get_mailer_config():
    """Get web mailer config from secrets or local file."""
    if "web_hunter" in st.secrets:
        s = st.secrets["web_hunter"]
        return {
            'email_address': s.get("mailer_email", ""),
            'app_password': s.get("mailer_password", ""),
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'your_name': s.get("mailer_name", ""),
            'your_company': s.get("mailer_company", "")
        }
    elif IS_LOCAL:
        cfg_path = os.path.join(LEAD_PULLER_DIR, "config_mailer.json")
        if os.path.exists(cfg_path):
            with open(cfg_path) as f:
                return json.load(f)
    return None

def load_sheet_data(sheet):
    """Load data from a gspread worksheet into a DataFrame."""
    try:
        data = sheet.get_all_values()
        if not data: return pd.DataFrame()
        headers = data[0]
        rows = data[1:]
        seen = {}
        new_headers = []
        for h in headers:
            if h in seen:
                seen[h] += 1
                new_headers.append(f"{h}_{seen[h]}")
            else:
                seen[h] = 0
                new_headers.append(h)
        return pd.DataFrame(rows, columns=new_headers)
    except:
        return pd.DataFrame()

def load_web_templates():
    """Load web templates from local JSON or return defaults."""
    if IS_LOCAL:
        tpl_path = os.path.join(LEAD_PULLER_DIR, "templates.json")
        if os.path.exists(tpl_path):
            try:
                with open(tpl_path) as f: return json.load(f)
            except: pass
    return DEFAULT_WEB_TEMPLATES.copy()

def save_web_templates(templates):
    """Save web templates to local JSON if local, otherwise no-op."""
    if IS_LOCAL:
        tpl_path = os.path.join(LEAD_PULLER_DIR, "templates.json")
        with open(tpl_path, 'w') as f: json.dump(templates, f, indent=2)

def load_fleet_templates():
    """Load fleet JSON templates."""
    if IS_LOCAL:
        tp = os.path.join(TRUCK_SCRAPER_DIR, "templates", "fleet_templates.json")
        if os.path.exists(tp):
            with open(tp) as f: return json.load(f)
    # Default fallback if file missing
    return {
        "welcome": {"subject": "Welcome", "body": "Hi {contact_name}, welcome!"},
        "followup_1": {"subject": "Follow up", "body": "Checking in..."},
        "followup_2": {"subject": "Final check", "body": "Last attempt..."}
    }

def wrap_fleet_html(body_text):
    """Wraps plain text body in HTML with Logo and Flyer."""
    return f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto;">
        <p>{body_text.replace(chr(10), '<br>')}</p>
        <br>
        <p><img src="cid:logo_image" alt="Jayboi Services" width="200"></p>
        <p><img src="cid:flyer_image" alt="Services Flyer" width="100%"></p>
    </div>
</body>
</html>"""

def save_fleet_templates(data):
    """Save fleet JSON templates."""
    if IS_LOCAL:
        tp = os.path.join(TRUCK_SCRAPER_DIR, "templates", "fleet_templates.json")
        with open(tp, 'w') as f: json.dump(data, f, indent=4)

def parse_last_sent_web(df):
    """Parse last sent date from Web Hunter data."""
    dates = []
    for col in ["Lead Status", "Last Contacted"]:
        if col in df.columns:
            for val in df[col]:
                val = str(val)
                # Try date formats like "2026-02-05" or "Email 1 Sent (2026-02-05)" or "Contacted"
                import re
                match = re.search(r'(\d{4}-\d{2}-\d{2})', val)
                if match:
                    dates.append(match.group(1))
    return max(dates) if dates else "Never"

def parse_last_sent_fleet(df):
    """Parse last sent date from Fleet Manager data."""
    dates = []
    if "Status" in df.columns:
        import re
        for val in df["Status"]:
            match = re.search(r'(\d{4}-\d{2}-\d{2})', str(val))
            if match:
                dates.append(match.group(1))
    return max(dates) if dates else "Never"

# ==========================================
# DATA LOADING
# ==========================================

# ==========================================
# DATA LOADING (CACHED)
# ==========================================

@st.cache_data(ttl=600)
def get_web_data():
    """Fetch all Web Hunter data, cached for 10 mins."""
    web_client = get_web_client()
    if not web_client:
        return pd.DataFrame(), "❌ Not Configured"
    
    try:
        sheet_name = "Lead Puller Master List"
        if "web_hunter" in st.secrets:
            sheet_name = st.secrets["web_hunter"].get("sheet_name", sheet_name)
        
        sh = web_client.open(sheet_name)
        ws_name = "Website Leads"
        if "web_hunter" in st.secrets:
            ws_name = st.secrets["web_hunter"].get("worksheet_name", ws_name)
            
        web_worksheet = sh.worksheet(ws_name)
        df = load_sheet_data(web_worksheet)
        return df, "✅ Online"
    except Exception as e:
        return pd.DataFrame(), f"⚠️ {str(e)[:40]}"

@st.cache_data(ttl=600)
def get_fleet_data():
    """Fetch all Fleet Manager data, cached for 10 mins."""
    fleet_client = get_fleet_client()
    fleet_sheet_id = get_fleet_sheet_id()
    
    if not fleet_client or not fleet_sheet_id:
        return pd.DataFrame(), "❌ Not Configured"
        
    try:
        fleet_sh = fleet_client.open_by_key(fleet_sheet_id)
        fleet_worksheet = fleet_sh.sheet1
        df = pd.DataFrame(fleet_worksheet.get_all_records())
        return df, "✅ Online"
    except Exception as e:
        return pd.DataFrame(), f"⚠️ {str(e)[:40]}"

# Load Data
web_df, web_health = get_web_data()
fleet_df, fleet_health = get_fleet_data()

# Calculate Stats
web_total = len(web_df)
web_last_sent = parse_last_sent_web(web_df)
fleet_total = len(fleet_df)
fleet_last_sent = parse_last_sent_fleet(fleet_df)

# Need worksheets object for updates (not cached)
# We re-fetch the worksheet object only when needed for writes
# to avoid serializing the socket connection in cache_data
def get_active_web_worksheet():
    try:
        client = get_web_client()
        if not client: return None
        sheet_name = "Lead Puller Master List"
        if "web_hunter" in st.secrets:
            sheet_name = st.secrets["web_hunter"].get("sheet_name", sheet_name)
        sh = client.open(sheet_name)
        ws_name = "Website Leads"
        if "web_hunter" in st.secrets:
            ws_name = st.secrets["web_hunter"].get("worksheet_name", ws_name)
        return sh.worksheet(ws_name)
    except:
        return None

def get_active_fleet_worksheet():
    try:
        client = get_fleet_client()
        fid = get_fleet_sheet_id()
        if not client or not fid: return None
        return client.open_by_key(fid).sheet1
    except:
        return None

web_worksheet = get_active_web_worksheet()
fleet_worksheet = get_active_fleet_worksheet()


# ==========================================
# SIDEBAR: GLOBAL SETTINGS
# ==========================================
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Automation Toggle (using Sheet as DB)
    if "web_worksheet" in locals() and web_worksheet:
        try:
            # Try to get/create Config sheet
            client = get_web_client()
            sheet_id = get_web_sheet_id()
            
            config_ws = None
            if client:
                try:
                    if sheet_id and len(sheet_id) > 20:
                        config_ws = client.open_by_key(sheet_id).worksheet("Config")
                        wb = client.open_by_key(sheet_id)
                    else:
                        # Fallback to Name (Default for this user)
                        wb = client.open(sheet_name)
                        
                    try:
                        config_ws = wb.worksheet("Config")
                    except:
                        config_ws = wb.add_worksheet("Config", 10, 2)
                        config_ws.update([["Automation Status", "Value"], ["Global", "ACTIVE"]], "A1")
                except Exception as e_inner:
                    # st.caption(f"DB Connect: {e_inner}")
                    pass
                
                if config_ws:
                    # Read Status
                    try:
                        current_status = config_ws.acell("B2").value
                        is_active = (str(current_status).strip().upper() != "PAUSED")
                        
                        # Toggle
                        new_state = st.toggle("🟢 Automation Active", value=is_active)
                        
                        # Update if changed
                        if new_state != is_active:
                            new_val = "ACTIVE" if new_state else "PAUSED"
                            config_ws.update_acell("B2", new_val)
                            st.toast(f"Automation set to {new_val}")
                            time.sleep(1)
                            st.rerun()
                            
                        if not is_active:
                            st.error("🛑 Automation PAUSED")
                    except:
                        pass
        except Exception as e:
            st.caption(f"Config Sync: {str(e)[:20]}...")

# ... (Existing Sidebar)
    # Automation Toggle (using Sheet as DB)
    if "web_worksheet" in locals() and web_worksheet:
        # ... (Existing Automation Logic) ...
        pass # Placeholder to keep context if needed, but we are appending mainly

    st.divider()
    st.markdown("### 🛡️ Data Safety")
    if st.button("💾 Backup Data Now"):
        with st.spinner("Backing up Leads, Invoices & Credit Data..."):
            try:
                import subprocess
                backup_script = os.path.join(os.path.dirname(__file__), '../../scripts/daily_backup.py')
                result = subprocess.run(["python3", backup_script], capture_output=True, text=True)
                if result.returncode == 0:
                    st.success("✅ Backup Complete!")
                    st.toast("Backup saved to Empire_Data", icon="💾")
                else:
                    st.error(f"Backup Failed: {result.stderr}")
            except Exception as e:
                st.error(f"Error running backup: {e}")

# ... (Rest of App) ...

# ------------------------------------------------------------------
# TAB 3: FLEET MANAGER (Updated Campaign Logic)
# ------------------------------------------------------------------
# ... (Inside fleet_sub_campaign) ...
        with fleet_sub_campaign:
            st.subheader("🚀 Fleet Auto-Blaster")
            
            # Identify candidates: Status='New', Type='C', has Email
            candidates = []
            if "Status" in fleet_df.columns and "Type" in fleet_df.columns and "Email" in fleet_df.columns:
                for i, r in fleet_df.iterrows():
                    status = str(r.get("Status", "")).strip().lower()
                    auth_type = str(r.get("Type", "")).strip().upper()
                    email = str(r.get("Email", "")).strip()
                    if status == "new" and auth_type == "C" and email and email.lower() not in ['n/a', 'none', '', 'nan']:
                        candidates.append({'idx': i + 2, 'name': r.get('Legal Name', 'Carrier'), 'email': email, 'dot': str(r.get('DOT#', ''))})
            
            st.metric("Ready to Blast", len(candidates))
            blast_limit = st.slider("Blast Limit", 1, 50, 10, key="blast_slider")
            
            # Get fleet mailer creds ... (Existing Creds Logic) ...
            fleet_user = ""
            fleet_pass = ""
            fleet_from = ""
            if "fleet_manager" in st.secrets:
                fleet_user = st.secrets["fleet_manager"].get("gmail_username", "")
                fleet_pass = st.secrets["fleet_manager"].get("gmail_app_password", "")
                fleet_from = st.secrets["fleet_manager"].get("from_email", fleet_user)
            elif IS_LOCAL:
                try:
                    from dotenv import dotenv_values
                    env = dotenv_values(os.path.join(TRUCK_SCRAPER_DIR, ".env"))
                    fleet_pass = env.get("GMAIL_APP_PASSWORD", "").strip('"')
                    fleet_user = "Theboiblazin2026@gmail.com"
                    fleet_from = "Info@jayboiservicesllc.com"
                except:
                    pass
            
            if not fleet_pass:
                st.warning("Fleet mailer credentials not found.")
            
            # SESSION STATE FOR CAMPAIGN RESULTS
            if 'fleet_campaign_results' not in st.session_state:
                st.session_state.fleet_campaign_results = None

            if st.button("🚀 LAUNCH FLEET CAMPAIGN") and fleet_pass:
                st.warning("⚠️ Sending Real Emails...")
                prog = st.progress(0)
                status_box = st.container()
                
                # Load "Welcome" template for new blasts
                templates = load_fleet_templates()
                welcome_tmpl = templates.get("welcome", {})
                start_subj = welcome_tmpl.get("subject", "Welcome to the Industry")
                start_body = welcome_tmpl.get("body", "Hi {contact_name}")
                
                try:
                    smtp = smtplib.SMTP("smtp.gmail.com", 587)
                    smtp.starttls()
                    smtp.login(fleet_user, fleet_pass)
                except Exception as e:
                    st.error(f"SMTP Error: {e}")
                    smtp = None
                
                if smtp:
                    sent_count = 0
                    failed_count = 0
                    logs = []
                    
                    for idx, lead in enumerate(candidates[:blast_limit]):
                        # Personalize
                        try:
                            subj = start_subj.format(company_name=lead['name'], contact_name="Manager", dot_number=lead['dot'])
                            body_txt = start_body.format(company_name=lead['name'], contact_name="Manager", dot_number=lead['dot'])
                            body_html = wrap_fleet_html(body_txt)
                        except:
                            subj = start_subj
                            body_html = wrap_fleet_html(start_body)
                        
                        try:
                            msg = MIMEMultipart('related')
                            msg['From'] = f"Jayboi Services <{fleet_from}>" if fleet_from else fleet_user
                            msg['To'] = lead['email']
                            msg['Subject'] = subj
                            
                            alt = MIMEMultipart('alternative')
                            msg.attach(alt)
                            alt.attach(MIMEText("Please view in HTML.", 'plain'))
                            alt.attach(MIMEText(body_html, 'html'))
                            
                            # Attach images if local
                            if IS_LOCAL:
                                for cid, fname in [('logo_image', 'logo.png'), ('flyer_image', 'flyer.png')]:
                                    img_path = os.path.join(TRUCK_SCRAPER_DIR, 'templates', fname)
                                    if os.path.exists(img_path):
                                        with open(img_path, 'rb') as f:
                                            img = MIMEImage(f.read())
                                        img.add_header('Content-ID', f'<{cid}>')
                                        img.add_header('Content-Disposition', 'inline')
                                        msg.attach(img)
                            
                            recipients = [lead['email'], fleet_user]
                            smtp.sendmail(fleet_user, recipients, msg.as_string())
                            
                            # Update sheet
                            fleet_worksheet.update_cell(lead['idx'], 10, f"Emailed: {datetime.date.today()}")
                            sent_count += 1
                            logs.append(f"✅ Sent: {lead['name']}")
                            # status_box.text(f"✅ Sent to {lead['name']}")
                        except Exception as e:
                            failed_count += 1
                            logs.append(f"❌ Failed: {lead['name']} - {e}")
                            # status_box.text(f"❌ Failed: {lead['name']} — {e}")
                        
                        prog.progress((idx + 1) / min(blast_limit, len(candidates)))
                        time.sleep(2)
                    
                    smtp.quit()
                    
                    # Store results in session state
                    st.session_state.fleet_campaign_results = {
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                        "sent": sent_count,
                        "failed": failed_count,
                        "logs": logs
                    }
                    st.rerun()

            # Show Persistent Results
            if st.session_state.fleet_campaign_results:
                res = st.session_state.fleet_campaign_results
                st.success(f"🎉 Campaign Finished at {res['timestamp']}")
                c1, c2 = st.columns(2)
                c1.metric("✅ Sent", res['sent'])
                c2.metric("❌ Failed", res['failed'])
                
                with st.expander("View Campaign Logs", expanded=True):
                    for log in res['logs']:
                        st.text(log)
                
                if st.button("Clear Results"):
                    st.session_state.fleet_campaign_results = None
                    st.rerun()
    else:
        st.info("Fleet Manager not connected. Check credentials in secrets or connect SSD.")
tab_dash, tab_web, tab_fleet = st.tabs(["📊 Dashboard", "🌐 Web Hunter", "🚛 Fleet Manager"])

# ------------------------------------------------------------------
# TAB 1: DASHBOARD
# ------------------------------------------------------------------
with tab_dash:
    st.header("System Health & Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌐 Web Hunter")
        st.markdown(f"**Status:** {web_health}")
        
        # Velocity Chart
        try:
            if "Timestamp" in web_df.columns:
                 web_df["Date"] = pd.to_datetime(web_df["Timestamp"], errors='coerce').dt.date
                 vel = web_df.groupby("Date").size().reset_index(name="Leads")
                 fig = px.bar(vel, x="Date", y="Leads", title="Lead Velocity", color_discrete_sequence=["#00CC96"])
                 fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
                 st.plotly_chart(fig, use_container_width=True)
            else:
                 st.metric("Total Leads", web_total)
        except:
            st.metric("Total Leads", web_total)

        web_replies = len(web_df[web_df['Lead Status'].str.contains("Replied", case=False, na=False)]) if "Lead Status" in web_df.columns else 0
        web_rate = (web_replies / web_total * 100) if web_total > 0 else 0
        st.metric("Reply Rate", f"{web_rate:.1f}% ({web_replies})")
        st.caption(f"Last Sent: {web_last_sent}")
        
        with st.expander("System Checks"):
            has_creds = "web_hunter" in st.secrets or (IS_LOCAL and os.path.exists(os.path.join(LEAD_PULLER_DIR, "service_account.json")))
            has_mailer = "web_hunter" in st.secrets or (IS_LOCAL and os.path.exists(os.path.join(LEAD_PULLER_DIR, "config_mailer.json")))
            st.checkbox("Google Auth", value=has_creds, disabled=True)
            st.checkbox("Mailer Config", value=has_mailer, disabled=True)
            st.checkbox("Sheet Connected", value="Online" in web_health, disabled=True)

    with col2:
        st.subheader("🚛 Fleet Manager")
        st.markdown(f"**Status:** {fleet_health}")
        
        # Pipeline Health
        try:
            if "Status" in fleet_df.columns:
                stats = fleet_df["Status"].value_counts().reset_index()
                stats.columns = ["Status", "Count"]
                fig = px.pie(stats, names="Status", values="Count", title="Pipeline Status", hole=0.4)
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.metric("Total Carriers", fleet_total)
        except:
             st.metric("Total Carriers", fleet_total)

        fleet_replies = len(fleet_df[fleet_df['Status'].str.contains("Replied", case=False, na=False)]) if "Status" in fleet_df.columns else 0
        fleet_rate = (fleet_replies / fleet_total * 100) if fleet_total > 0 else 0
        st.metric("Reply Rate", f"{fleet_rate:.1f}% ({fleet_replies})")
        st.caption(f"Last Sent: {fleet_last_sent}")
        
        with st.expander("System Checks"):
            has_fleet = "fleet_manager" in st.secrets or (IS_LOCAL and os.path.exists(os.path.join(TRUCK_SCRAPER_DIR, ".env")))
            st.checkbox("Fleet Auth", value=has_fleet, disabled=True)
            st.checkbox("Sheet Connected", value="Online" in fleet_health, disabled=True, key="fleet_sheet_check")

    st.divider()
    env_label = "🟢 Running Locally (SSD Connected)" if IS_LOCAL else "☁️ Running on Cloud"
    st.info(f"**Environment:** {env_label}")

# ------------------------------------------------------------------
# TAB 2: WEB HUNTER
# ------------------------------------------------------------------
with tab_web:
    if "Online" in web_health:
        st.success(f"🟢 {web_health} | Last Sent: {web_last_sent}")
    else:
        st.error(f"🔴 {web_health}")

    web_sub_data, web_sub_studio, web_sub_campaign = st.tabs(["📊 Data", "📧 Email Studio", "🚀 Campaign"])
    
    if web_worksheet is not None:
        # --- DATA VIEW ---
        with web_sub_data:
            c1, c2, c3 = st.columns([1, 1, 3])
            with c1:
                if st.button("🔄 Refresh"):
                    get_web_data.clear()
                    st.rerun()
            with c2:
                if "Address" in web_df.columns:
                    states = ["All"] + sorted(set(s for s in ["GA","TX","CA","FL","IL","TN","OH","NY","NC"] if web_df["Address"].str.contains(s, na=False).any()))
                    state_f = st.selectbox("State", states)
                else:
                    state_f = "All"
            with c3:
                search = st.text_input("🔍 Search", placeholder="Company name...")
            
            filtered = web_df.copy()
            if state_f != "All" and "Address" in filtered.columns:
                filtered = filtered[filtered["Address"].str.contains(state_f, case=False, na=False)]
            if search and "Business Name" in filtered.columns:
                filtered = filtered[filtered["Business Name"].str.contains(search, case=False, na=False)]
            
            st.dataframe(filtered, use_container_width=True, height=800)
            st.caption(f"Showing {len(filtered)} of {web_total}")

        # --- EMAIL STUDIO ---
        with web_sub_studio:
            st.header("Web Lead Templates")
            templates = load_web_templates()
            t_type = st.selectbox("Template", ["standard", "broken_link", "not_secure"], format_func=lambda x: x.replace('_',' ').title())
            curr = templates.get(t_type, {})
            
            with st.form("web_tmpl"):
                if t_type == "standard":
                    curr["subject_a"] = st.text_input("Subject A", curr.get("subject_a", ""))
                    curr["subject_b"] = st.text_input("Subject B", curr.get("subject_b", ""))
                else:
                    curr["subject"] = st.text_input("Subject", curr.get("subject", ""))
                curr["body"] = st.text_area("Body", curr.get("body", ""), height=250)
                st.caption("Variables: `{business_name}`, `{city}`, `{sender_name}`")
                
                if st.form_submit_button("💾 Save"):
                    templates[t_type] = curr
                    save_web_templates(templates)
                    st.success("Saved!")

            st.divider()
            st.subheader("🧪 Test Mode")
            test_config = get_mailer_config()
            default_test = test_config.get('email_address', '') if test_config else ""
            test_email = st.text_input("Send Test To", value=default_test)
            

            if st.button("📨 Send Test Email"):
                if not test_config:
                    st.error("Mailer not configured.")
                else:
                    try:
                        server = smtplib.SMTP(test_config['smtp_server'], test_config['smtp_port'])
                        server.starttls()
                        server.login(test_config['email_address'], test_config['app_password'])
                        
                        # Mock variables
                        sender = test_config.get('your_name', 'Me')
                        subj = "[TEST] " + (curr.get("subject_a") if t_type == "standard" else curr.get("subject"))
                        body_txt = curr.get("body", "").format(business_name="Test Business", city="Test City", sender_name=sender)
                        
                        # Use Fleet HTML wrapper for consistency
                        body_html = wrap_fleet_html(body_txt)

                        msg = MIMEMultipart('related')
                        msg['From'] = test_config['email_address']
                        msg['To'] = test_email
                        msg['Subject'] = subj
                        
                        alt = MIMEMultipart('alternative')
                        msg.attach(alt)
                        alt.attach(MIMEText("Please view in HTML.", 'plain'))
                        alt.attach(MIMEText(body_html, 'html'))

                        # Attach Images (Logo + Flyer) - Local Only Check
                        if IS_LOCAL:
                             for cid, fname in [('logo_image', 'logo.png'), ('flyer_image', 'flyer.png')]:
                                img_path = os.path.join(LEAD_PULLER_DIR, 'templates', fname)
                                if os.path.exists(img_path):
                                    with open(img_path, 'rb') as f:
                                        img = MIMEImage(f.read())
                                    img.add_header('Content-ID', f'<{cid}>')
                                    img.add_header('Content-Disposition', 'inline')
                                    msg.attach(img)
                        
                        server.sendmail(test_config['email_address'], test_email, msg.as_string())
                        server.quit()
                        st.success(f"Sent test to {test_email}")
                    except Exception as e:
                        st.error(f"Test Failed: {e}")

        # --- CAMPAIGN ---
        with web_sub_campaign:
            st.subheader("Manual Web Campaign")
            config = get_mailer_config()
            
            if not config:
                st.warning("Mailer not configured. Add credentials to secrets.")
            elif "Lead Status" in web_df.columns:
                eligible = web_df[
                    (web_df["Emails Found"] != "") & 
                    (~web_df["Lead Status"].str.contains("Contacted|Email 1|Sent", case=False, na=False))
                ]
                st.metric("New Leads with Email", len(eligible))
                
                tmpls = load_web_templates()
                std = tmpls.get("standard", {})
                st.text(f"Preview Subject: {std.get('subject_a','')}")
                
                batch_size = st.slider("Batch Size", 1, 20, 5)
                
                if st.button("🚀 Run Drip Campaign"):
                    with st.spinner("⏳ Processing Drip Sequence..."):
                         try:
                             # Import local manager (lazy load)
                             sys.path.append(os.path.join(os.path.dirname(__file__), '../../pocket_leads'))
                             from campaign_manager import CampaignManager
                             
                             cm = CampaignManager(config)
                             
                             # 1. Get Eligible
                             eligible = cm.get_eligible_leads(web_df, max_leads=batch_size)
                             
                             if not eligible:
                                 st.info("✅ All caught up! No leads due for action today.")
                             else:
                                 # 2. Process
                                 tmpls = load_web_templates()
                                 res = cm.process_queue(eligible, web_worksheet, tmpls)
                                 
                                 st.success(f"Processed {len(eligible)} leads")
                                 with st.expander("Campaign Logs", expanded=True):
                                     for log in res.get("logs", []):
                                         st.text(log)
                                         
                                 if res.get("sent", 0) > 0:
                                     time.sleep(2)
                                     st.rerun()
                         except Exception as e:
                             st.error(f"Campaign Error: {e}")

# ------------------------------------------------------------------
# TAB 3: FLEET MANAGER
# ------------------------------------------------------------------
with tab_fleet:
    if "Online" in fleet_health:
        st.success(f"🟢 {fleet_health} | Last Sent: {fleet_last_sent}")
    else:
        st.error(f"🔴 {fleet_health}")

    st.header("🚛 Fleet Manager")
    fleet_sub_data, fleet_sub_studio, fleet_sub_campaign = st.tabs(["📊 Data", "📧 Email Studio", "🚀 Campaign"])
    
    if fleet_worksheet is not None:
        # --- FLEET DATA ---
        with fleet_sub_data:
            if st.button("🔄 Refresh FMCSA"):
                get_fleet_data.clear()
                st.rerun()
            
            cols = st.columns(3)
            with cols[0]:
                if "Status" in fleet_df.columns:
                    status_opts = ["All"] + sorted(fleet_df["Status"].unique().tolist())
                    status_f = st.selectbox("Status", status_opts)
                else:
                    status_f = "All"
            with cols[1]:
                type_f = st.selectbox("Auth Type", ["All", "C", "B", "P"])
            
            filtered_fleet = fleet_df.copy()
            if status_f != "All" and "Status" in filtered_fleet.columns:
                filtered_fleet = filtered_fleet[filtered_fleet["Status"] == status_f]
            if type_f != "All" and "Type" in filtered_fleet.columns:
                filtered_fleet = filtered_fleet[filtered_fleet["Type"] == type_f]
            
            st.dataframe(filtered_fleet, use_container_width=True, height=800)
            st.caption(f"Showing {len(filtered_fleet)} of {fleet_total}")

        # --- FLEET EMAIL STUDIO ---
        with fleet_sub_studio:
            st.subheader("Fleet Email Template")
            
            # Load current HTML or default
            # Load Templates
            templates = load_fleet_templates()
            
            # Template Selector
            t_opts = ["welcome", "followup_1", "followup_2"]
            t_sel = st.selectbox("Select Stage", t_opts, format_func=lambda x: x.replace("_", " ").title())
            
            current_tmpl = templates.get(t_sel, {})
            
            with st.form("fleet_email_form"):
                st.write(f"Editing: **{t_sel.replace('_', ' ').title()}**")
                
                new_subj = st.text_input("Subject Line", current_tmpl.get("subject", ""))
                new_body = st.text_area("Email Body", value=current_tmpl.get("body", ""), height=300)
                
                st.caption("Variables: `{contact_name}`, `{company_name}`, `{dot_number}`")
                
                if st.form_submit_button("💾 Save Template"):
                    templates[t_sel] = {"subject": new_subj, "body": new_body}
                    save_fleet_templates(templates)
                    st.success(f"Saved {t_sel} template!")
                    time.sleep(1)
                    st.success(f"Saved {t_sel} template!")
                    time.sleep(1)
                    st.rerun()

            st.divider()
            st.subheader("🧪 Test Mode")
            
            # Load Creds for Test
            test_fleet_user = ""
            test_fleet_pass = ""
            if "fleet_manager" in st.secrets:
                test_fleet_user = st.secrets["fleet_manager"].get("gmail_username", "")
                test_fleet_pass = st.secrets["fleet_manager"].get("gmail_app_password", "")
            elif IS_LOCAL:
                try:
                    from dotenv import dotenv_values
                    env = dotenv_values(os.path.join(TRUCK_SCRAPER_DIR, ".env"))
                    test_fleet_pass = env.get("GMAIL_APP_PASSWORD", "").strip('"')
                    test_fleet_user = "Theboiblazin2026@gmail.com"
                except: pass

            test_to = st.text_input("Send Test To", value=test_fleet_user, key="fleet_test_to")
            
            if st.button("📨 Send Test Fleet Email") and test_fleet_pass:
                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(test_fleet_user, test_fleet_pass)
                    
                    # Construct
                    subj = "[TEST] " + current_tmpl.get("subject", "")
                    body_txt = current_tmpl.get("body", "").format(contact_name="Test Manager", company_name="Test Corp", dot_number="000000")
                    html = wrap_fleet_html(body_txt)
                    
                    msg = MIMEMultipart('related')
                    msg['From'] = test_fleet_user
                    msg['To'] = test_to
                    msg['Subject'] = subj
                    
                    # Attach HTML
                    alt = MIMEMultipart('alternative')
                    msg.attach(alt)
                    alt.attach(MIMEText("HTML Required", 'plain'))
                    alt.attach(MIMEText(html, 'html'))
                    
                    # Attach Images (Local only for test unless we map paths)
                    # For simplicity in test mode on cloud, we might skip images or try to load them
                    # If local, attach.
                    if IS_LOCAL:
                         for cid, fname in [('logo_image', 'logo.png'), ('flyer_image', 'flyer.png')]:
                            img_path = os.path.join(TRUCK_SCRAPER_DIR, 'templates', fname)
                            if os.path.exists(img_path):
                                with open(img_path, 'rb') as f:
                                    img = MIMEImage(f.read())
                                img.add_header('Content-ID', f'<{cid}>')
                                msg.attach(img)

                    server.sendmail(test_fleet_user, test_to, msg.as_string())
                    server.quit()
                    st.success(f"Test sent to {test_to}")
                except Exception as e:
                    st.error(f"Test failed: {e}")

            st.divider()
            st.subheader("Preview")
            # Simple preview of the body text
            st.subheader("Preview")
            st.markdown(f"**Subject:** {current_tmpl.get('subject', '')}")
            st.info(current_tmpl.get('body', '').format(contact_name="John Doe", company_name="Acme Trucking", dot_number="1234567"))

        # --- FLEET CAMPAIGN ---
        with fleet_sub_campaign:
            st.subheader("🚀 Fleet Auto-Blaster")
            
            # Identify candidates: Status='New', Type='C', has Email
            candidates = []
            for i, r in fleet_df.iterrows():
                status = str(r.get("Status", "")).strip().lower()
                auth_type = str(r.get("Type", "")).strip().upper()
                email = str(r.get("Email", "")).strip()
                if status == "new" and auth_type == "C" and email and email.lower() not in ['n/a', 'none', '', 'nan']:
                    candidates.append({'idx': i + 2, 'name': r.get('Legal Name', 'Carrier'), 'email': email, 'dot': str(r.get('DOT#', ''))})
            
            st.metric("Ready to Blast", len(candidates))
            blast_limit = st.slider("Blast Limit", 1, 50, 10, key="blast_slider")
            
            # Get fleet mailer creds
            fleet_user = ""
            fleet_pass = ""
            fleet_from = ""
            if "fleet_manager" in st.secrets:
                fleet_user = st.secrets["fleet_manager"].get("gmail_username", "")
                fleet_pass = st.secrets["fleet_manager"].get("gmail_app_password", "")
                fleet_from = st.secrets["fleet_manager"].get("from_email", fleet_user)
            elif IS_LOCAL:
                # Read from .env
                try:
                    from dotenv import dotenv_values
                    env = dotenv_values(os.path.join(TRUCK_SCRAPER_DIR, ".env"))
                    fleet_pass = env.get("GMAIL_APP_PASSWORD", "").strip('"')
                    fleet_user = "Theboiblazin2026@gmail.com"
                    fleet_from = "Info@jayboiservicesllc.com"
                except:
                    pass
            
            if not fleet_pass:
                st.warning("Fleet mailer credentials not found.")
            
            if st.button("🚀 LAUNCH FLEET CAMPAIGN") and fleet_pass:
                st.warning("⚠️ Sending Real Emails...")
                prog = st.progress(0)
                status_text = st.empty()
                
                # Load "Welcome" template for new blasts
                templates = load_fleet_templates()
                welcome_tmpl = templates.get("welcome", {})
                start_subj = welcome_tmpl.get("subject", "Welcome to the Industry")
                start_body = welcome_tmpl.get("body", "Hi {contact_name}")
                
                try:
                    smtp = smtplib.SMTP("smtp.gmail.com", 587)
                    smtp.starttls()
                    smtp.login(fleet_user, fleet_pass)
                except Exception as e:
                    st.error(f"SMTP Error: {e}")
                    smtp = None
                
                if smtp:
                    sent_count = 0
                    for idx, lead in enumerate(candidates[:blast_limit]):
                        # Personalize
                        try:
                            subj = start_subj.format(company_name=lead['name'], contact_name="Manager", dot_number=lead['dot'])
                            body_txt = start_body.format(company_name=lead['name'], contact_name="Manager", dot_number=lead['dot'])
                            body_html = wrap_fleet_html(body_txt)
                        except:
                            subj = start_subj
                            body_html = wrap_fleet_html(start_body)
                        
                        try:
                            msg = MIMEMultipart('related')
                            msg['From'] = f"Jayboi Services <{fleet_from}>"
                            msg['To'] = lead['email']
                            msg['Subject'] = subj
                            
                            alt = MIMEMultipart('alternative')
                            msg.attach(alt)
                            alt.attach(MIMEText("Please view in HTML.", 'plain'))
                            alt.attach(MIMEText(body_html, 'html'))
                            
                            # Attach images if local
                            if IS_LOCAL:
                                for cid, fname in [('logo_image', 'logo.png'), ('flyer_image', 'flyer.png')]:
                                    img_path = os.path.join(TRUCK_SCRAPER_DIR, 'templates', fname)
                                    if os.path.exists(img_path):
                                        with open(img_path, 'rb') as f:
                                            img = MIMEImage(f.read())
                                        img.add_header('Content-ID', f'<{cid}>')
                                        img.add_header('Content-Disposition', 'inline')
                                        msg.attach(img)
                            
                            recipients = [lead['email'], fleet_user]
                            smtp.sendmail(fleet_user, recipients, msg.as_string())
                            
                            # Update sheet
                            fleet_worksheet.update_cell(lead['idx'], 10, f"Emailed: {datetime.date.today()}")
                            sent_count += 1
                            status_text.text(f"✅ Sent to {lead['name']}")
                        except Exception as e:
                            status_text.text(f"❌ Failed: {lead['name']} — {e}")
                        
                        prog.progress((idx + 1) / min(blast_limit, len(candidates)))
                        time.sleep(2)
                    
                    smtp.quit()
                    st.success(f"🎉 Blast Complete! Sent {sent_count} emails.")
                    time.sleep(2)
                    st.rerun()
    else:
        st.info("Fleet Manager not connected. Check credentials in secrets or connect SSD.")