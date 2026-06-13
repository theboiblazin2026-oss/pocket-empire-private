import streamlit as st
import os
import sys
import json
import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
from pydantic import BaseModel, Field
from typing import List, Optional

# --- Pydantic Models for Structured OCR Outputs ---
class RateConDetails(BaseModel):
    load_no: str = Field(description="The Load Number or PO Number of the rate confirmation.")
    date: Optional[str] = Field(description="The date of the rate confirmation or date booked (YYYY-MM-DD format if possible).")
    route: str = Field(description="The complete route (e.g. Norcross, GA - Palos Heights, IL).")
    broker: str = Field(description="The company name of the broker (e.g. TQL, C.H. Robinson).")
    base_rate: float = Field(description="The gross base rate paid (numeric only).")
    miles: Optional[float] = Field(description="Total loaded miles or trip distance. Default to 0 if not found.")

class SettledLoad(BaseModel):
    load_no: str = Field(description="The Load / PO # of the settled load (e.g., PO# 16164).")
    base_rate: float = Field(description="The base gross rate of the load (e.g. 3000.00).")
    amount: float = Field(description="The driver's cut / earned amount for this load (e.g. 930.00).")

class SettlementTransaction(BaseModel):
    description: str = Field(description="The description of the transaction (e.g., '[CADV] Cash Advance', 'Escrow', 'Sign On Bonus').")
    amount: float = Field(description="The amount. Negative for deductions, positive for awards/salary additions (e.g., -200.00, 250.00).")

class SettlementDetails(BaseModel):
    week_ending_date: Optional[str] = Field(description="The date of the settlement or week ending date (YYYY-MM-DD format if possible).")
    driver_name: str = Field(description="The driver's name (e.g. Calvin Manning).")
    loads: List[SettledLoad] = Field(description="The list of all loads settled on this statement.")
    transactions: List[SettlementTransaction] = Field(description="The list of all additions and deductions on this statement.")
    net_pay: float = Field(description="The final net pay paid to the driver.")

# --- Page Configuration ---
st.set_page_config(
    page_title="Driver Load Tracker & Auditor",
    page_icon="🚚",
    layout="wide"
)

# --- Find Credentials File Robustly ---
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, "../.."))
LOCAL_CREDS_PATH = os.path.join(root_dir, "service_account.json")
SYSTEM_CREDS_PATH = "/Users/newguy/.gemini/service_account.json"

# API Key Resolution
api_key = "AIzaSyDniw4SdcQE6dZSWt7wGapY4dxu6j9SloY" # System Fallback

# 1. Try Secrets
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
elif os.getenv("GOOGLE_API_KEY"):
    api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)

# Connect to Google Sheets
@st.cache_resource
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 1. Try Streamlit Secrets (Cloud)
    if "gcp_service_account" in st.secrets:
        try:
            creds_info = json.loads(st.secrets["gcp_service_account"])
            creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"Failed to load service account info from st.secrets: {e}")
            
    # 2. Try Local Root Path
    if os.path.exists(LOCAL_CREDS_PATH):
        try:
            creds = Credentials.from_service_account_file(LOCAL_CREDS_PATH, scopes=scopes)
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"Failed to load credentials from {LOCAL_CREDS_PATH}: {e}")
            
    # 3. Try System Path
    if os.path.exists(SYSTEM_CREDS_PATH):
        try:
            creds = Credentials.from_service_account_file(SYSTEM_CREDS_PATH, scopes=scopes)
            return gspread.authorize(creds)
        except Exception as e:
            st.error(f"Failed to load credentials from {SYSTEM_CREDS_PATH}: {e}")

    st.error("❌ Google Sheets API credentials not found! Please check service_account.json.")
    return None

gc = get_gspread_client()
SHEET_NAME = "Driver Pay Settlement Tracker"

# --- Main App ---
st.title("🚚 Driver Load Tracker & Settlement Auditor")
st.caption("Keep track of your loads, auto-deductions, and reconcile your weekly carrier paychecks.")

if gc:
    try:
        sh = gc.open(SHEET_NAME)
        st.sidebar.success(f"Connected to Google Sheet: {SHEET_NAME}")
        st.sidebar.link_button("📂 Open Spreadsheet in Google Sheets", sh.url)
    except gspread.SpreadsheetNotFound:
        st.error(f"❌ Spreadsheet '{SHEET_NAME}' was NOT found.")
        st.info(f"""
        Please do the following:
        1. Create a blank Google Sheet named exactly: **{SHEET_NAME}**
        2. Share it with Editor permissions to this service account:
           `lead-agent@jay-leads-2026.iam.gserviceaccount.com`
        3. Refresh this page to initialize the tracker.
        """)
        st.stop()
        
    tabs = st.tabs(["📤 Rate Con OCR", "📝 Manual Load Entry", "⚖️ Settlement Auditor", "📊 View Ledger"])

    # ------------------ TAB 1: RATE CON OCR ------------------
    with tabs[0]:
        st.header("Extract Rate Confirmation Details")
        st.caption("Upload a Rate Con PDF or Image saved from Telegram or your phone to automatically parse details.")
        
        uploaded_rate_con = st.file_uploader("Upload Rate Con (PDF/PNG/JPG)", type=["pdf", "png", "jpg", "jpeg"], key="rate_con_uploader")
        
        if uploaded_rate_con:
            if st.button("🔍 Parse Rate Confirmation"):
                with st.spinner("Analyzing document with Gemini AI..."):
                    try:
                        file_bytes = uploaded_rate_con.getvalue()
                        mime_type = uploaded_rate_con.type
                        
                        # Call Gemini OCR
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        prompt = "Extract the Rate Confirmation details in JSON format."
                        file_part = {"mime_type": mime_type, "data": file_bytes}
                        
                        response = model.generate_content(
                            [file_part, prompt],
                            generation_config=genai.GenerationConfig(
                                response_mime_type="application/json",
                                response_schema=RateConDetails
                            )
                        )
                        
                        extracted = json.loads(response.text)
                        st.session_state["extracted_rate_con"] = extracted
                        st.success("✅ Extracted successfully! Review details below.")
                    except Exception as e:
                        st.error(f"OCR failed: {e}")

        # Edit Form
        if "extracted_rate_con" in st.session_state:
            data = st.session_state["extracted_rate_con"]
            st.divider()
            st.subheader("Edit & Verify Load Details")
            
            col1, col2 = st.columns(2)
            with col1:
                load_no = st.text_input("Load / PO #", value=data.get("load_no", ""))
                dates = st.text_input("Dates", value=data.get("date", datetime.date.today().strftime("%m/%d/%Y")))
                week_ending = st.text_input("Week Ending Date (Sunday)", value=datetime.date.today().strftime("%Y-%m-%d"))
                route = st.text_input("Route / Details", value=data.get("route", ""))
                pay_type = st.selectbox("Pay Type", ["Percentage", "Hourly"], index=0)
            
            with col2:
                base_pay = st.number_input("Base Gross Pay ($)", value=float(data.get("base_rate", 0.0)), step=50.0)
                hours_worked = st.number_input("Hours Worked (if Hourly)", value=0.0, step=1.0)
                hourly_rate = st.number_input("Hourly Rate ($/hr)", value=30.00, step=1.0)
                driver_rate_pct = st.number_input("Driver Rate %", value=31.0, step=0.5)
            
            if st.button("💾 Save Load to Google Sheets", key="save_ocr_load"):
                with st.spinner("Appending to Google Sheets..."):
                    try:
                        ws_load_log = sh.worksheet("Load Log")
                        
                        # Find first empty row (looking at Load # column)
                        all_rows = ws_load_log.get_all_values()
                        next_row = len(all_rows) + 1
                        
                        # Prepare data row
                        # Columns match: Load #, Dates, Week Ending, Route, Pay Type, Hours, Hourly Rate, Base Gross, Driver Rate%, Earned, Actual, Discrepancy, Completed?
                        # Note: Google Sheets index starts at 2 for row formulas
                        pct_decimal = driver_rate_pct / 100.0
                        row_data = [
                            load_no, dates, week_ending, route, pay_type, hours_worked,
                            f"=Settings!B$9", base_pay, pct_decimal,
                            f'=IF(E{next_row}="Percentage", H{next_row}*I{next_row}, F{next_row}*G{next_row})',
                            "", f"=K{next_row}-J{next_row}", "FALSE"
                        ]
                        
                        ws_load_log.insert_row(row_data, next_row, value_input_option="USER_ENTERED")
                        st.success(f"✅ Load {load_no} saved successfully in row {next_row}!")
                        del st.session_state["extracted_rate_con"]
                    except Exception as e:
                        st.error(f"Failed to write to Google Sheets: {e}")

    # ------------------ TAB 2: MANUAL LOAD ENTRY ------------------
    with tabs[1]:
        st.header("Log Load / Shift Manually")
        st.caption("Type in load details or hourly shift information manually.")
        
        with st.form("manual_load_form"):
            col1, col2 = st.columns(2)
            with col1:
                m_load_no = st.text_input("Load / PO # (or 'HOURLY')")
                m_dates = st.date_input("Date(s)")
                m_week_ending = st.date_input("Week Ending Date (Sunday)")
                m_route = st.text_input("Route / Details", placeholder="Norcross, GA - Palos Heights, IL or Hourly Shift")
                m_pay_type = st.selectbox("Pay Type", ["Percentage", "Hourly"])
            
            with col2:
                m_base_pay = st.number_input("Base Gross Pay ($)", min_value=0.0, step=50.0)
                m_hours_worked = st.number_input("Hours Worked (if Hourly)", min_value=0.0, step=1.0)
                m_hourly_rate = st.number_input("Hourly Rate ($/hr) override", value=30.00)
                m_driver_rate_pct = st.number_input("Driver Rate % override", value=31.0)
            
            submitted = st.form_submit_button("Save Load")
            
            if submitted:
                with st.spinner("Appending to Google Sheets..."):
                    try:
                        ws_load_log = sh.worksheet("Load Log")
                        all_rows = ws_load_log.get_all_values()
                        next_row = len(all_rows) + 1
                        
                        row_data = [
                            m_load_no, m_dates.strftime("%m/%d/%Y"), m_week_ending.strftime("%Y-%m-%d"), 
                            m_route, m_pay_type, m_hours_worked, f"=Settings!B$9", m_base_pay, 
                            m_driver_rate_pct / 100.0,
                            f'=IF(E{next_row}="Percentage", H{next_row}*I{next_row}, F{next_row}*G{next_row})',
                            "", f"=K{next_row}-J{next_row}", "FALSE"
                        ]
                        
                        ws_load_log.insert_row(row_data, next_row, value_input_option="USER_ENTERED")
                        st.success(f"✅ Load {m_load_no} saved successfully in row {next_row}!")
                    except Exception as e:
                        st.error(f"Failed to write to Google Sheets: {e}")

    # ------------------ TAB 3: SETTLEMENT AUDITOR ------------------
    with tabs[2]:
        st.header("Forensic Settlement Auditor")
        st.caption("Upload your carrier pay statement PDF to automatically cross-check it against your logged loads.")
        
        uploaded_settlement = st.file_uploader("Upload Settlement Statement (PDF)", type=["pdf"], key="settlement_uploader")
        
        if uploaded_settlement:
            if st.button("⚖️ Run Settlement Audit"):
                with st.spinner("Extracting and reconciling pay details with Gemini AI..."):
                    try:
                        file_bytes = uploaded_settlement.getvalue()
                        
                        # Call Gemini to parse Settlement PDF
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        prompt = "Analyze this carrier Settlement Statement document and extract the loads and transactions details."
                        file_part = {"mime_type": "application/pdf", "data": file_bytes}
                        
                        response = model.generate_content(
                            [file_part, prompt],
                            generation_config=genai.GenerationConfig(
                                response_mime_type="application/json",
                                response_schema=SettlementDetails
                            )
                        )
                        
                        settlement = json.loads(response.text)
                        st.session_state["parsed_settlement"] = settlement
                        st.success("✅ Settlement parsed successfully! Generating Reconciliation Report...")
                    except Exception as e:
                        st.error(f"Parsing failed: {e}")

        # Reconciliation Report
        if "parsed_settlement" in st.session_state:
            s_data = st.session_state["parsed_settlement"]
            st.divider()
            
            st.subheader(f"📄 Reconciliation Report: {s_data.get('driver_name', 'Calvin Manning')}")
            st.write(f"**Settlement Week/Date:** {s_data.get('week_ending_date', 'N/A')}")
            
            # Fetch Load Log from Google Sheets to compare
            ws_load_log = sh.worksheet("Load Log")
            load_log_data = ws_load_log.get_all_records()
            df_log = pd.DataFrame(load_log_data)
            
            # Reconcile Loads
            settled_loads = s_data.get("loads", [])
            
            st.markdown("### 🔍 Load Reconciliation Details")
            
            discrepancies = []
            matched_pos = []
            
            table_rows = []
            for load in settled_loads:
                po = load.get("load_no", "").strip().replace("PO#", "").replace("PO", "").strip()
                s_base = load.get("base_rate", 0.0)
                s_amount = load.get("amount", 0.0)
                
                # Try to find match in spreadsheet
                match = None
                if not df_log.empty:
                    # Fuzzy match on PO #
                    df_log['clean_po'] = df_log['Load / PO #'].astype(str).str.replace("PO#", "").str.replace("PO", "").str.strip()
                    matched_rows = df_log[df_log['clean_po'] == po]
                    if not matched_rows.empty:
                        match = matched_rows.iloc[0]
                
                if match is not None:
                    expected = float(match['Earned Driver Pay']) if match['Earned Driver Pay'] != "" else 0.0
                    diff = s_amount - expected
                    matched_pos.append(match['Load / PO #'])
                    
                    if abs(diff) < 0.05:
                        status = "✅ Match"
                    else:
                        status = f"❌ Discrepancy (${diff:+.2f})"
                        discrepancies.append(f"Load {po} pay discrepancy: expected ${expected:.2f}, paid ${s_amount:.2f}")
                        
                    table_rows.append({
                        "PO #": load.get("load_no"),
                        "Route / Details": match.get("Route / Details", "Match Found"),
                        "Expected Pay": f"${expected:.2f}",
                        "Settled Pay": f"${s_amount:.2f}",
                        "Status": status
                    })
                else:
                    status = "⚠️ Missing from Ledger (Not Logged by You)"
                    table_rows.append({
                        "PO #": load.get("load_no"),
                        "Route / Details": "Unknown (Not in your log)",
                        "Expected Pay": "$0.00",
                        "Settled Pay": f"${s_amount:.2f}",
                        "Status": status
                    })
            
            # Check for logged loads that are missing in the settlement statement
            if not df_log.empty and s_data.get("week_ending_date"):
                # Filter log by week ending date
                week_target = s_data.get("week_ending_date")
                df_week = df_log[df_log['Week Ending'] == week_target]
                for idx, row in df_week.iterrows():
                    logged_po = str(row['Load / PO #'])
                    if logged_po not in matched_pos:
                        expected = float(row['Earned Driver Pay']) if row['Earned Driver Pay'] != "" else 0.0
                        discrepancies.append(f"Load {logged_po} is missing from Settlement! You are owed ${expected:.2f}")
                        table_rows.append({
                            "PO #": logged_po,
                            "Route / Details": row['Route / Details'],
                            "Expected Pay": f"${expected:.2f}",
                            "Settled Pay": "$0.00",
                            "Status": "❌ Omitted from Settlement (Unpaid)"
                        })
            
            st.table(pd.DataFrame(table_rows))
            
            # Additions and Deductions Reconciliation
            st.markdown("### 💸 Additions & Deductions")
            txs = s_data.get("transactions", [])
            tx_rows = []
            for tx in txs:
                tx_rows.append({
                    "Description": tx.get("description"),
                    "Amount": f"${tx.get('amount'):+.2f}"
                })
            st.table(pd.DataFrame(tx_rows))
            
            # Net paycheck match summary
            st.divider()
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Statement Net Pay", f"${s_data.get('net_pay'):,.2f}")
            with col2:
                if not discrepancies:
                    st.success("🎉 **Audit Passed!** Your settlement matches your logged loads exactly.")
                else:
                    st.error(f"⚠️ **Discrepancies Detected:** We found {len(discrepancies)} mismatching items.")
                    for disc in discrepancies:
                        st.write(f"- {disc}")
            
            # Reconcile Action Button
            if st.button("🔒 Apply Reconciliation to Google Sheets"):
                with st.spinner("Updating spreadsheet ledger..."):
                    try:
                        # 1. Update Load Log with Actual Settled Amounts
                        ws_load_log = sh.worksheet("Load Log")
                        load_vals = ws_load_log.get_all_values()
                        
                        for load in settled_loads:
                            po = load.get("load_no", "").strip().replace("PO#", "").replace("PO", "").strip()
                            s_amount = load.get("amount", 0.0)
                            
                            # Find matching row index (1-indexed, headers are row 1)
                            for idx, row in enumerate(load_vals):
                                if idx == 0: continue
                                logged_po = row[0].replace("PO#", "").replace("PO", "").strip()
                                if logged_po == po:
                                    # Update column K (Actual Settled Pay) and M (Completed)
                                    ws_load_log.update_cell(idx + 1, 11, s_amount) # K
                                    ws_load_log.update_cell(idx + 1, 13, "TRUE") # M
                                    break
                                    
                        # 2. Add Variable Transactions into Deductions & Awards Log
                        ws_deductions_log = sh.worksheet("Deductions & Awards Log")
                        d_rows = ws_deductions_log.get_all_values()
                        next_d_row = len(d_rows) + 1
                        
                        added_txs = 0
                        for tx in txs:
                            desc = tx.get("description", "")
                            amt = tx.get("amount", 0.0)
                            
                            # Skip standard auto-deductions (Escrow, Occ Acc) which are config-lookup based
                            if "escrow" in desc.lower() or "accident insurance" in desc.lower():
                                continue
                                
                            row_d = [
                                datetime.date.today().strftime("%m/%d/%Y"),
                                s_data.get('week_ending_date', ''),
                                "Bonus" if amt > 0 else "Cash Advance",
                                desc,
                                amt
                            ]
                            ws_deductions_log.insert_row(row_d, next_d_row, value_input_option="USER_ENTERED")
                            next_d_row += 1
                            added_txs += 1
                            
                        # 3. Update Weekly Settlements table with Actual Paid Amount and Audit Status
                        ws_settlements = sh.worksheet("Weekly Settlements")
                        settle_vals = ws_settlements.get_all_values()
                        week_target = s_data.get('week_ending_date', '')
                        
                        updated_settle = False
                        for idx, row in enumerate(settle_vals):
                            if idx == 0: continue
                            if row[0] == week_target:
                                # Update Actual Paid Amount (G) and Audit Status (I)
                                ws_settlements.update_cell(idx + 1, 7, s_data.get('net_pay')) # G
                                status_str = "Match" if not discrepancies else "Discrepancy"
                                ws_settlements.update_cell(idx + 1, 9, status_str) # I
                                updated_settle = True
                                break
                                
                        if not updated_settle:
                            # Add a new row in settlements if the week ending date wasn't listed yet
                            next_s_row = len(settle_vals) + 1
                            row_s = [
                                week_target,
                                f"=SUMIFS('Load Log'!J:J, 'Load Log'!C:C, A{next_s_row})",
                                f"=SUMIFS('Deductions & Awards Log'!E:E, 'Deductions & Awards Log'!B:B, A{next_s_row}, 'Deductions & Awards Log'!E:E, \">0\")",
                                "=SUMIF(Settings!C$3:C$4, TRUE, Settings!B$3:B$4)",
                                f"=ABS(SUMIFS('Deductions & Awards Log'!E:E, 'Deductions & Awards Log'!B:B, A{next_s_row}, 'Deductions & Awards Log'!E:E, \"<0\"))",
                                f"=B{next_s_row}+C{next_s_row}-D{next_s_row}-E{next_s_row}",
                                s_data.get('net_pay'),
                                f"=G{next_s_row}-F{next_s_row}",
                                "Match" if not discrepancies else "Discrepancy"
                            ]
                            ws_settlements.insert_row(row_s, next_s_row, value_input_option="USER_ENTERED")
                            
                        st.success("✅ Google Sheets successfully updated! Reconciliation saved.")
                        del st.session_state["parsed_settlement"]
                    except Exception as e:
                        st.error(f"Reconciliation write failed: {e}")

    # ------------------ TAB 4: VIEW LEDGER ------------------
    with tabs[3]:
        st.header("Ledger Status")
        st.caption("View live sheets from your Google Drive.")
        
        selected_ws = st.selectbox("Select Tab to View", ["Weekly Settlements", "Load Log", "Deductions & Awards Log", "Settings"])
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()
            
        with st.spinner("Fetching data from Google Sheets..."):
            try:
                ws = sh.worksheet(selected_ws)
                data = ws.get_all_values()
                if data:
                    df = pd.DataFrame(data[1:], columns=data[0])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("This tab is currently empty.")
            except Exception as e:
                st.error(f"Error fetching worksheet: {e}")
else:
    st.info("Please set up Google API credentials inside service_account.json to load the app.")
