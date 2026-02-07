import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import smtplib
import json
import time
import random
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

# --- Page Config ---
try:
    st.set_page_config(page_title="The Prospector", page_icon="⛏️", layout="wide")
except:
    pass

st.title("⛏️ The Prospector")
st.caption("Lead Puller Command Center")

# --- Configuration ---
# Path to the "Lead Puller" project on the SSD
LEAD_PULLER_DIR = "/Volumes/CeeJay SSD/Projects/lead puller"
CREDS_FILE = os.path.join(LEAD_PULLER_DIR, "service_account.json")

# --- Functions ---
def get_client():
    if not os.path.exists(CREDS_FILE):
        st.error(f"❌ Service Account JSON not found at: {CREDS_FILE}")
        return None
    
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    client = gspread.authorize(creds)
    return client

def repair_headers(sheet):
    """Refactored logic from repair_leads_sheet.py"""
    headers = sheet.row_values(1)
    clean_headers = ['Business Name', 'Industry', 'Website', 'Secure (SSL)', 'Emails Found', 'Socials', 'Contact Link', 'Status', 'Phone', 'Address', 'Date Added', 'Last Contacted', 'Lead Status']
    
    if headers != clean_headers:
        st.warning(f"⚠️ Headers Mismatch found.")
        st.write(f"Current: {headers}")
        st.write(f"Target: {clean_headers}")
        
        if st.button("🔧 Fix Headers Now"):
            if len(headers) < len(clean_headers):
                sheet.resize(cols=len(clean_headers))
            sheet.update('A1:M1', [clean_headers])
            sheet.freeze(rows=1)
            st.success("✅ Headers Updated & Frozen!")
            st.rerun()
    else:
        st.success("✅ Headers are Healthy.")

def load_data(sheet):
    # Fetch raw data to avoid gspread's unique header check
    data = sheet.get_all_values()
    if not data:
        return pd.DataFrame()
        
    headers = data[0]
    rows = data[1:]
    
    # Dedup headers
    seen = {}
    new_headers = []
    for h in headers:
        if h in seen:
            seen[h] += 1
            new_headers.append(f"{h}_{seen[h]}")
        else:
            seen[h] = 0
            new_headers.append(h)
            
    df = pd.DataFrame(rows, columns=new_headers)
    df = pd.DataFrame(rows, columns=new_headers)
    return df

# --- Mailer Logic ---
class Mailer:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        
    def load_config(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return None
        
    def connect(self):
        if not self.config: return None
        try:
            server = smtplib.SMTP(self.config.get('smtp_server', 'smtp.gmail.com'), self.config.get('smtp_port', 587))
            server.starttls()
            server.login(self.config['email_address'], self.config['app_password'])
            return server
        except Exception as e:
            st.error(f"SMTP Error: {e}")
            return None

    def generate_email(self, lead):
        # Template logic from external script
        name = lead.get('Business Name', 'Business Owner')
        city = "your area"
        address = str(lead.get('Address', ''))
        if "GA" in address: city = "Atlanta area" # Simple fallback
        
        subject = f"Are you accepting new jobs in {city}?"
        body = f"Hi,\n\nAre you taking on new work in {city} right now?\n\nI have a system that brings in consistent jobs for {name}, and I'm looking for one partner in the area.\n\nOpen to a quick chat?\n\nBest,\n{self.config.get('your_name', 'Tech Trap')}"
        return subject, body

# --- Display Logic ---

if not os.path.exists(LEAD_PULLER_DIR):
    st.error(f"❌ Cannot find Lead Puller Directory: {LEAD_PULLER_DIR}")
    st.info("Ensure the SSD is connected.")
    st.stop()

if "client" not in st.session_state:
    st.session_state.client = get_client()

if st.session_state.client:
    try:
        # Open user's sheet
        # Note: Name is hardcoded in repair_leads_sheet.py as "Lead Puller Master List"
        sh = st.session_state.client.open("Lead Puller Master List")
        worksheet = sh.worksheet("Website Leads")
        
        # 1. Header Health Check
        with st.expander("🔧 Diagnostics & Repair", expanded=False):
            repair_headers(worksheet)
            
        # 2. Data View
        st.subheader("📊 Lead Database")
        
        # Filters row
        f1, f2, f3 = st.columns([1, 1, 2])
        with f1:
            if st.button("🔄 Refresh Data"):
                st.rerun()
        
        df = load_data(worksheet)
        
        # State Filter
        with f2:
            states = ["All States", "GA", "TX", "CA", "FL", "IL", "TN", "OH", "PA", "NY", "NJ", 
                      "NC", "IN", "MO", "AZ", "NV", "WA", "CO", "VA", "MD", "LA", "AL", "KY", 
                      "SC", "MS", "AR", "OK", "KS", "UT", "OR", "MI", "MN", "WI", "IA", "NE"]
            state_filter = st.selectbox("Filter by State", states)
        
        # Company Search
        with f3:
            company_search = st.text_input("🔍 Search Company", placeholder="Type company name...")
        
        # Apply filters
        filtered_df = df.copy()
        
        if state_filter != "All States" and "Address" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Address"].str.contains(state_filter, case=False, na=False)]
        
        if company_search and "Business Name" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Business Name"].str.contains(company_search, case=False, na=False)]
        
        # Show filtered count
        st.caption(f"Showing {len(filtered_df)} of {len(df)} leads")
        st.dataframe(filtered_df, use_container_width=True, height=600)
        
        # 3. Stats
        st.sidebar.header("Stats")
        st.sidebar.metric("Total Leads", len(df))
        if "Emails Found" in df.columns:
            emails_count = len(df[df["Emails Found"] != ""])
            st.sidebar.metric("Emails Found", emails_count)

        # 4. Campaign Manager
        st.subheader("🚀 Campaign Manager")
        with st.expander("Launch Campaign", expanded=True):
            mailer_config_path = os.path.join(LEAD_PULLER_DIR, "config_mailer.json")
            if not os.path.exists(mailer_config_path):
                st.error("Config missing!")
            else:
                mailer = Mailer(mailer_config_path)
                
                # Check Eligible
                if "Lead Status" not in df.columns:
                    st.warning("Column 'Lead Status' missing. Run 'Repair Headers' first.")
                else:
                    # Filter for NEW leads with emails
                    eligible = df[
                        (df["Emails Found"] != "") & 
                        (~df["Lead Status"].str.contains("Contacted", case=False, na=False)) &
                        (~df["Lead Status"].str.contains("Email 1", case=False, na=False))
                    ]
                    
                    st.metric("Eligible for Email 1", len(eligible))
                    
                    # --- Templates ---
                    st.markdown("### 📝 Email Template")
                    default_subject = "Are you accepting new jobs in {city}?"
                    default_body = """Hi,

Are you taking on new work in {city} right now?

I have a system that brings in consistent jobs for {name}, and I'm looking for one partner in the area.

Open to a quick chat?

Best,
{sender_name}"""
                    
                    subject_template = st.text_input("Subject Line", value=default_subject)
                    body_template = st.text_area("Email Body", value=default_body, height=200)
                    st.caption("Variables: `{name}`, `{city}`, `{sender_name}`")
                    
                    batch_size = st.slider("Batch Size", 1, 20, 5)
                    
                    if st.button("📤 Send Batch Now"):
                        conn = mailer.connect()
                        if conn:
                            progress = st.progress(0)
                            status_text = st.empty()
                            
                            to_send = eligible.head(batch_size)
                            sent_count = 0
                            
                            for index, row in to_send.iterrows():
                                # Prepare Variables
                                name = row.get('Business Name', 'Business Owner')
                                address = str(row.get('Address', ''))
                                city = "your area"
                                if "GA" in address: city = "Atlanta area"
                                sender_name = mailer.config.get('your_name', 'Tech Trap')
                                
                                # Render Template
                                final_subject = subject_template.format(name=name, city=city, sender_name=sender_name)
                                final_body = body_template.format(name=name, city=city, sender_name=sender_name)

                                email = row["Emails Found"].split(',')[0].strip()
                                
                                try:
                                    msg = MIMEMultipart()
                                    msg['From'] = mailer.config['email_address']
                                    msg['To'] = email
                                    msg['Subject'] = final_subject
                                    msg.attach(MIMEText(final_body, 'plain'))
                                    
                                    conn.sendmail(mailer.config['email_address'], email, msg.as_string())
                                    
                                    # Update Sheet
                                    cell = worksheet.find(row["Business Name"])
                                    if cell:
                                        worksheet.update_cell(cell.row, 13, f"Email 1 Sent ({datetime.date.today()})") 
                                    
                                    sent_count += 1
                                    progress.progress((index + 1) / batch_size)
                                    status_text.text(f"Sent to {row['Business Name']}")
                                    time.sleep(2) # Rate limit
                                    
                                except Exception as e:
                                    st.error(f"Failed to send to {row['Business Name']}: {e}")
                                    
                            conn.quit()
                            st.success(f"Batch Complete! Sent {sent_count} emails.")
                            st.rerun()

    except Exception as e:
        st.error(f"Error accessing Google Sheet: {e}")
