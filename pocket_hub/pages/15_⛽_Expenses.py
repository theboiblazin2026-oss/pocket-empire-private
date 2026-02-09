
import streamlit as st
import pandas as pd
import os
import sys
import datetime
import shutil

# Database path (reuse invoices/financials data or new?)
# Let's use a simple JSON for expenses first to be fast, or reuse wealth manager?
# Wealth Manager tracks "Income Streams", but expenses are usually business deducutions.
# Let's create `pocket_invoices/expenses.json`

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../pocket_invoices'))
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")

import json

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

st.set_page_config(page_title="Expenses", page_icon="⛽", layout="wide")

st.title("⛽ Expense Tracker")
st.caption("Log Fuel, Maintenance, and Business Expenses for Tax Deductions.")

# --- Stats ---
expenses = load_expenses()
df = pd.DataFrame(expenses)

if not df.empty:
    df['amount'] = pd.to_numeric(df['amount'])
    df['date'] = pd.to_datetime(df['date'])
    
    total_exp = df['amount'].sum()
    this_month = df[df['date'].dt.month == datetime.datetime.now().month]['amount'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Expenses (YTD)", f"${total_exp:,.2f}")
    c2.metric("This Month", f"${this_month:,.2f}")
    c3.metric("Transactions", len(df))

st.divider()

# --- Entry Form ---
st.subheader("📝 Log New Expense")

with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date")
        category = st.selectbox("Category", ["⛽ Fuel", "🔧 Maintenance", "🍔 Meals", "🏨 Lodging", "🛡️ Insurance", "📞 Phone/Internet", "🖊️ Office", "Other"])
        merchant = st.text_input("Merchant / Pilot / Love's", placeholder="Pilot Travel Center")
    
    with col2:
        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        receipt = st.file_uploader("📸 Receipt Photo", type=["jpg", "png", "pdf"])
        notes = st.text_area("Notes", height=100)
    
    if st.form_submit_button("💾 Save Expense", type="primary"):
        # Save logic
        new_exp = {
            "id": datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
            "date": str(date),
            "category": category,
            "merchant": merchant,
            "amount": amount,
            "notes": notes,
            "receipt_path": "" 
        }
        
        # Save receipt if uploaded
        if receipt:
            # Create uploads dir
            uploads_dir = os.path.join(DATA_DIR, "receipts")
            os.makedirs(uploads_dir, exist_ok=True)
            
            ext = receipt.name.split('.')[-1]
            fname = f"{new_exp['id']}_receipt.{ext}"
            fpath = os.path.join(uploads_dir, fname)
            
            with open(fpath, "wb") as f:
                f.write(receipt.getbuffer())
                
            new_exp['receipt_path'] = fpath
            
        expenses.append(new_exp)
        save_expenses(expenses)
        st.success("Expense Saved!")
        st.rerun()

st.divider()

# --- Table View ---
st.subheader("📜 Recent Transactions")

if not df.empty:
    # Display table with formatting
    display_df = df[['date', 'category', 'merchant', 'amount', 'notes', 'receipt_path']].sort_values(by='date', ascending=False)
    
    # Custom column config
    st.dataframe(
        display_df,
        column_config={
            "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
            "receipt_path": st.column_config.LinkColumn("Receipt"),
        },
        use_container_width=True
    )
else:
    st.info("No expenses logged yet.")
