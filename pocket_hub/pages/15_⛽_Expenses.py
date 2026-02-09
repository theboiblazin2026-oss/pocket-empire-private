
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

import pandas as pd
import os
import sys
import datetime
import json
import shutil
from PIL import Image

# Setup Paths
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_invoices'))
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")

# Ensure Data Dir Exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# --- Logic ---

def load_expenses():
    if not os.path.exists(EXPENSES_FILE):
        return []
    try:
        with open(EXPENSES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_expenses(data):
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def scan_receipt_with_ai(file_bytes):
    """Scan receipt using local LLM."""
    try:
        import ollama
    except ImportError:
        return None  # Ollama not installed
    
    try:
        # Save temp file
        temp_path = "temp_receipt.jpg"
        with open(temp_path, "wb") as f:
            f.write(file_bytes)
            
        prompt = """
        Analyze this receipt. Extract these fields as JSON:
        - date (YYYY-MM-DD)
        - merchant (Name)
        - amount (Total float)
        - gallons (If fuel, float. Else 0)
        - state (2-letter US state code, e.g. TX. Infer from address if needed)
        
        Return ONLY JSON. No markdown.
        """
        
        response = ollama.chat(model='llava', messages=[
            {'role': 'user', 'content': prompt, 'images': [temp_path]}
        ])
        
        content = response['message']['content']
        # Clean code blocks
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
        
    except Exception as e:
        print(f"AI Error: {e}")
        return None

# --- UI ---

st.set_page_config(page_title="Expenses & IFTA", page_icon="⛽", layout="wide")

st.title("⛽ Expenses & IFTA")
st.caption("Track Fuel, Receipts, and Quarterly IFTA Taxes.")

tab1, tab2, tab3 = st.tabs(["📝 Log Expense", "📊 IFTA Report", "📜 History"])

# Load Data
expenses = load_expenses()
df = pd.DataFrame(expenses)

# Fix Data Types if DF Exists
if not df.empty:
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df['gallons'] = pd.to_numeric(df.get('gallons', 0), errors='coerce').fillna(0)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')


# --- TAB 1: LOG EXPENSE ---
with tab1:
    st.subheader("New Transaction")
    
    # Session State for AI Pre-fill
    if 'exp_form_data' not in st.session_state:
        st.session_state.exp_form_data = {}
        
    # AI Uploader
    with st.expander("📸 Scan Receipt (AI Auto-Fill)", expanded=True):
        uploaded_file = st.file_uploader("Upload Receipt", type=["jpg", "png", "jpeg"])
        if uploaded_file and st.button("✨ Scan with AI"):
            with st.spinner("Reading Receipt..."):
                extracted = scan_receipt_with_ai(uploaded_file.getvalue())
                if extracted:
                    st.success("Read Successful!")
                    st.session_state.exp_form_data = extracted
                else:
                    st.error("Could not read receipt. Enter manually.")
    
    # Form
    with st.form("expense_form", clear_on_submit=True):
        # Pre-fill defaults
        defaults = st.session_state.exp_form_data
        
        col1, col2 = st.columns(2)
        with col1:
            # Date
            d_val = datetime.date.today()
            if defaults.get('date'):
                try: d_val = datetime.datetime.strptime(defaults['date'], "%Y-%m-%d").date()
                except: pass
            date = st.date_input("Date", value=d_val)
            
            # Merchant
            merchant = st.text_input("Merchant", value=defaults.get('merchant', ""), placeholder="Pilot / Shell")
            
            # Category
            cat_idx = 0
            OPTIONS = ["⛽ Fuel", "🔧 Maintenance", "🍔 Meals", "🏨 Lodging", "🛡️ Insurance", "🚙 Lease/Rent", "📞 Phone", "OTHER"]
            # Try to match AI inferred category (not rigorous, but fuel check helps)
            if defaults.get('gallons', 0) > 0: cat_idx = 0
            category = st.selectbox("Category", OPTIONS, index=cat_idx)
            
        with col2:
            # Amounts
            amount = st.number_input("Total Cost ($)", min_value=0.0, step=0.01, value=float(defaults.get('amount', 0.0)))
            
            # IFTA Fields (Show if Fuel)
            gallons = st.number_input("Gallons (IFTA)", min_value=0.0, step=0.1, value=float(defaults.get('gallons', 0.0)), help="Required for IFTA")
            
            # State
            states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD",
                      "MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC",
                      "SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
            
            s_idx = 0
            if defaults.get('state') and defaults['state'] in states:
                 s_idx = states.index(defaults['state'])
                 
            state = st.selectbox("State (IFTA)", states, index=s_idx)

        notes = st.text_area("Notes", height=60)
        
        if st.form_submit_button("💾 Save Transaction", type="primary"):
            new_exp = {
                "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                "date": str(date),
                "category": category,
                "merchant": merchant,
                "amount": amount,
                "gallons": gallons,
                "state": state,
                "notes": notes,
                "receipt_path": ""
            }
            
            # Save Receipt File
            if uploaded_file:
                uploads_dir = os.path.join(DATA_DIR, "receipts")
                os.makedirs(uploads_dir, exist_ok=True)
                fname = f"{new_exp['id']}_receipt.{uploaded_file.name.split('.')[-1]}"
                fpath = os.path.join(uploads_dir, fname)
                with open(fpath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                new_exp['receipt_path'] = fpath
                
            expenses.append(new_exp)
            save_expenses(expenses)
            
            # Clear scan cache
            st.session_state.exp_form_data = {}
            st.success("Saved!")
            st.rerun()

# --- TAB 2: IFTA REPORT ---
with tab2:
    st.markdown("### 🗺️ Quarterly IFTA Summary")
    
    if not df.empty:
        # Filter for Fuel only
        fuel_df = df[df['category'] == "⛽ Fuel"].copy()
        
        if fuel_df.empty:
            st.info("No fuel expenses logged yet.")
        else:
            # Group by State
            ifta = fuel_df.groupby('state')[['gallons', 'amount']].sum().reset_index()
            ifta['avg_price'] = ifta['amount'] / ifta['gallons']
            
            # Display
            st.dataframe(
                ifta,
                column_config={
                    "state": "State",
                    "gallons": st.column_config.NumberColumn("Total Gallons", format="%.1f gal"),
                    "amount": st.column_config.NumberColumn("Total Cost", format="$%.2f"),
                    "avg_price": st.column_config.NumberColumn("Avg Price/Gal", format="$%.3f"),
                },
                use_container_width=True
            )
            
            # Grand Totals
            c1, c2, c3 = st.columns(3)
            c1.metric("Total IFTA Gallons", f"{ifta['gallons'].sum():,.1f} gal")
            c2.metric("Total Fuel Cost", f"${ifta['amount'].sum():,.2f}")
            
            st.download_button(
                "📥 Download IFTA Report (CSV)",
                ifta.to_csv(index=False),
                "IFTA_Report.csv",
                "text/csv"
            )
    else:
        st.info("Log expenses to see IFTA data.")

# --- TAB 3: HISTORY ---
with tab3:
    st.subheader("📜 History")
    if not df.empty:
        # Display table with formatting
        display_df = df[['date', 'category', 'merchant', 'state', 'amount', 'gallons', 'receipt_path']].sort_values(by='date', ascending=False)
        
        st.dataframe(
            display_df,
            column_config={
                "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "receipt_path": st.column_config.LinkColumn("Receipt"),
            },
            use_container_width=True
        )
    else:
        st.info("No transactions.")