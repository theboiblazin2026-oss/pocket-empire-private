import streamlit as st
import sys
import os
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

def load_fleet_html_template():
    """Load fleet HTML email template."""
    if IS_LOCAL:
        tp = os.path.join(TRUCK_SCRAPER_DIR, "templates", "email_template.html")
        if os.path.exists(tp):
            with open(tp) as f: return f.read()
    # Fallback: embedded default
    return "<html><body><p>Hi {contact_name}, congrats on your new authority!</p></body></html>"

def save_fleet_html_template(html):
    """Save fleet HTML template."""
    if IS_LOCAL:
        tp = os.path.join(TRUCK_SCRAPER_DIR, "templates", "email_template.html")
        with open(tp, 'w') as f: f.write(html)

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
web_health = "Unknown"
fleet_health = "Unknown"
web_last_sent = "Checking..."
fleet_last_sent = "Checking..."
web_total = 0
fleet_total = 0
web_df = pd.DataFrame()
fleet_df = pd.DataFrame()

# --- WEB HUNTER DATA ---
web_client = get_web_client()
web_worksheet = None
if web_client:
    try:
        sheet_name = "Lead Puller Master List"
        if "web_hunter" in st.secrets:
            sheet_name = st.secrets["web_hunter"].get("sheet_name", sheet_name)
        sh = web_client.open(sheet_name)
        ws_name = "Website Leads"
        if "web_hunter" in st.secrets:
            ws_name = st.secrets["web_hunter"].get("worksheet_name", ws_name)
        web_worksheet = sh.worksheet(ws_name)
        web_df = load_sheet_data(web_worksheet)
        web_total = len(web_df)
        web_last_sent = parse_last_sent_web(web_df)
        web_health = "✅ Online"
    except Exception as e:
        web_health = f"⚠️ {str(e)[:40]}"
else:
    web_health = "❌ Not Configured"

# --- FLEET MANAGER DATA ---
fleet_client = get_fleet_client()
fleet_worksheet = None
fleet_sheet_id = get_fleet_sheet_id()
if fleet_client and fleet_sheet_id:
    try:
        fleet_sh = fleet_client.open_by_key(fleet_sheet_id)
        fleet_worksheet = fleet_sh.sheet1
        fleet_df = pd.DataFrame(fleet_worksheet.get_all_records())
        fleet_total = len(fleet_df)
        fleet_last_sent = parse_last_sent_fleet(fleet_df)
        fleet_health = "✅ Online"
    except Exception as e:
        fleet_health = f"⚠️ {str(e)[:40]}"
else:
    fleet_health = "❌ Not Configured"

# ==========================================
# APP LAYOUT (TABS)
# ==========================================
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
        st.metric("Total Leads", web_total)
        st.metric("Last Email Sent", web_last_sent)
        
        with st.expander("System Checks"):
            has_creds = "web_hunter" in st.secrets or (IS_LOCAL and os.path.exists(os.path.join(LEAD_PULLER_DIR, "service_account.json")))
            has_mailer = "web_hunter" in st.secrets or (IS_LOCAL and os.path.exists(os.path.join(LEAD_PULLER_DIR, "config_mailer.json")))
            st.checkbox("Google Auth", value=has_creds, disabled=True)
            st.checkbox("Mailer Config", value=has_mailer, disabled=True)
            st.checkbox("Sheet Connected", value="Online" in web_health, disabled=True)

    with col2:
        st.subheader("🚛 Fleet Manager")
        st.markdown(f"**Status:** {fleet_health}")
        st.metric("Total Carriers", fleet_total)
        st.metric("Last Email Sent", fleet_last_sent)
        
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
                if st.button("🔄 Refresh"): st.rerun()
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
            
            st.dataframe(filtered, use_container_width=True, height=500)
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
                
                if st.button("📤 Send Web Batch"):
                    try:
                        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
                        server.starttls()
                        server.login(config['email_address'], config['app_password'])
                    except Exception as e:
                        st.error(f"SMTP Error: {e}")
                        server = None
                    
                    if server:
                        prog = st.progress(0)
                        to_send = eligible.head(batch_size)
                        sent = 0
                        updates = []
                        today = datetime.date.today().strftime("%Y-%m-%d")
                        
                        for i, (idx, row) in enumerate(to_send.iterrows()):
                            name = row.get('Business Name', 'Owner')
                            email = row["Emails Found"].split(',')[0].strip()
                            sender = config.get('your_name', 'Tech Trap')
                            subj = std.get("subject_a", "Question").format(business_name=name, city="your area", sender_name=sender)
                            body = std.get("body", "").format(business_name=name, city="your area", sender_name=sender)
                            
                            try:
                                msg = MIMEMultipart()
                                msg['From'] = config['email_address']
                                msg['To'] = email
                                msg['Subject'] = subj
                                msg.attach(MIMEText(body, 'plain'))
                                server.sendmail(config['email_address'], email, msg.as_string())
                                
                                cell = web_worksheet.find(row["Business Name"])
                                if cell:
                                    updates.append({'range': f"L{cell.row}:M{cell.row}", 'values': [[today, "Contacted"]]})
                                sent += 1
                                prog.progress((i + 1) / len(to_send))
                                time.sleep(2)
                            except Exception as e:
                                st.error(f"Failed: {name} — {e}")
                        
                        server.quit()
                        if updates:
                            web_worksheet.batch_update(updates)
                        st.success(f"✅ Sent {sent} emails!")
                        time.sleep(1)
                        st.rerun()

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
            if st.button("🔄 Refresh FMCSA"): st.rerun()
            
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
            
            st.dataframe(filtered_fleet, use_container_width=True, height=500)
            st.caption(f"Showing {len(filtered_fleet)} of {fleet_total}")

        # --- FLEET EMAIL STUDIO ---
        with fleet_sub_studio:
            st.subheader("Fleet Email Template")
            
            # Load current HTML or default
            current_html = load_fleet_html_template()
            
            # Try to extract existing body text if it's a simple template
            default_body = "Hi {contact_name},\n\nCongrats on your new authority!\n\nWe provide comprehensive compliance services to keep you on the road and making money.\n\nLet us handle the paperwork so you can focus on driving.\n\nBest,\nJayboi Services LLC\n\"Your Compliance Company\""
            
            with st.form("fleet_email_form"):
                st.write("Edit your email content below. It will be automatically formatted nicely.")
                subject = st.text_input("Subject Line", "Welcome to the Industry: Essential Setup for {company_name}")
                body = st.text_area("Email Body", value=default_body, height=300)
                st.caption("Variables: `{contact_name}`, `{company_name}`, `{dot_number}`")
                
                if st.form_submit_button("💾 Save Template"):
                    # Wrap the plain text in the HTML structure
                    new_html = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto;">
        <p>{body.replace(chr(10), '<br>')}</p>
    </div>
</body>
</html>"""
                    save_fleet_html_template(new_html)
                    st.success("Template Saved!")
                    st.rerun()

            st.divider()
            st.subheader("Preview")
            # Simple preview of the body text
            st.info(body.format(contact_name="John Doe", company_name="Acme Trucking", dot_number="1234567"))

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
                
                html_tmpl = load_fleet_html_template()
                
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
                        subj = f"Welcome to the Industry: Essential Setup for {lead['name']}"
                        try:
                            body_html = html_tmpl.format(company_name=lead['name'], contact_name="Manager", dot_number=lead['dot'])
                        except:
                            body_html = html_tmpl
                        
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