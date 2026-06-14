import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import wealth_manager as wm
import importlib
importlib.reload(wm)
import client_manager as cm
import altair as alt
import os
import sys

# Add pocket_reminders to path for integration
reminders_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_reminders'))
if reminders_path not in sys.path:
    sys.path.insert(0, reminders_path)

try:
    import reminder_manager as rm
except ImportError:
    rm = None

def main():
    # --- Inject Custom CSS for Premium Glassmorphic Theme ---
    st.markdown("""
    <style>
        /* Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;600&display=swap');
        
        /* Font overrides */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
            font-family: 'Outfit', 'Inter', sans-serif !important;
        }
        
        /* Dark gradient background & glow */
        .stApp {
            background: radial-gradient(circle at 80% 10%, rgba(0, 255, 136, 0.04), transparent 45%),
                        radial-gradient(circle at 10% 90%, rgba(118, 75, 162, 0.04), transparent 45%),
                        #0B1A0B !important;
        }

        /* Glassmorphic Metrics and Alert blocks */
        div[data-testid="metric-container"], .metric-card, .element-container div.stAlert, div[data-testid="stExpander"] {
            background: rgba(26, 47, 26, 0.25) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 16px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            padding: 16px !important;
        }
        
        /* Expanders specific padding */
        div[data-testid="stExpander"] {
            padding: 0 !important;
            border-radius: 12px !important;
        }

        /* Metric hover state */
        div[data-testid="metric-container"]:hover {
            border-color: rgba(0, 255, 136, 0.25) !important;
            box-shadow: 0 8px 32px 0 rgba(0, 255, 136, 0.12) !important;
            transform: translateY(-2px);
        }

        /* Metric text styling */
        div[data-testid="metric-container"] label {
            color: #88A888 !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: #E8F5E9 !important;
        }

        /* Forms, inputs and dropdowns */
        div[data-baseweb="input"], div[data-baseweb="select"], .stTextArea textarea, .stNumberInput input, .stTextInput input {
            background-color: rgba(26, 47, 26, 0.5) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 8px !important;
            color: #E8F5E9 !important;
            transition: all 0.2s ease !important;
        }
        div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within, .stTextArea textarea:focus, .stNumberInput input:focus, .stTextInput input:focus {
            border-color: #00FF88 !important;
            box-shadow: 0 0 8px rgba(0, 255, 136, 0.4) !important;
        }

        /* Primary and secondary button designs */
        .stButton button, button[kind="primaryFormSubmit"], button[kind="secondaryFormSubmit"] {
            background: linear-gradient(135deg, #00FF88 0%, #00B36B 100%) !important;
            color: #0B1A0B !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 8px 20px !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 14px rgba(0, 255, 136, 0.25) !important;
        }
        .stButton button:hover, button[kind="primaryFormSubmit"]:hover, button[kind="secondaryFormSubmit"]:hover {
            transform: scale(1.02) !important;
            box-shadow: 0 6px 20px rgba(0, 255, 136, 0.4) !important;
            color: #0B1A0B !important;
        }
        .stButton button:active, button[kind="primaryFormSubmit"]:active, button[kind="secondaryFormSubmit"]:active {
            transform: scale(0.98) !important;
        }

        /* Bespoke Cockpit Navigation Card Buttons */
        .nav-card-container button {
            height: 140px !important;
            background: rgba(26, 47, 26, 0.25) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 16px !important;
            color: #E8F5E9 !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 20px !important;
        }
        .nav-card-container button div {
            font-size: 1.15rem !important;
            font-weight: 700 !important;
            text-align: center !important;
            line-height: 1.4 !important;
            white-space: pre-line !important;
        }
        .nav-card-container button:hover {
            border-color: #00FF88 !important;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.3) !important;
            transform: translateY(-2px) !important;
            color: #00FF88 !important;
        }
        .nav-card-container button:active {
            transform: scale(0.98) !important;
        }

        /* Overdue banner alert styling */
        .overdue-banner {
            background: rgba(255, 107, 107, 0.08) !important;
            border: 1px solid rgba(255, 107, 107, 0.25) !important;
            border-left: 5px solid #FF6B6B !important;
            border-radius: 12px !important;
            padding: 16px !important;
            margin-bottom: 24px !important;
            animation: pulse-glow 2s infinite ease-in-out;
        }
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 5px rgba(255, 107, 107, 0.15); }
            50% { box-shadow: 0 0 15px rgba(255, 107, 107, 0.4); }
        }

        /* Sidebar Glassmorphic Styling */
        section[data-testid="stSidebar"] {
            background-color: #071207 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        /* Table / dataframe overrides */
        div[data-testid="stDataFrame"] {
            background: rgba(26, 47, 26, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px !important;
        }
        
        /* Custom reminder list items */
        .reminder-overdue { border-left: 4px solid #FF6B6B !important; background: rgba(255, 107, 107, 0.05) !important; padding: 12px; border-radius: 8px; margin-bottom: 8px; }
        .reminder-due-soon { border-left: 4px solid #FFC107 !important; background: rgba(255, 193, 7, 0.05) !important; padding: 12px; border-radius: 8px; margin-bottom: 8px; }
        .reminder-upcoming { border-left: 4px solid #00FF88 !important; background: rgba(0, 255, 136, 0.05) !important; padding: 12px; border-radius: 8px; margin-bottom: 8px; }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Client Manager ---
    st.sidebar.title("👥 Client Manager")
    clients = cm.load_clients()
    client_names = ["My Personal Plan"] + [c["name"] for c in clients]
    selected_client_name = st.sidebar.selectbox("Select Profile", client_names)

    # Helper to get "My Plan" name
    if selected_client_name == "My Personal Plan":
        client_key = "myself"
        st.sidebar.info("Editing: Your Personal Wealth Plan")
    else:
        client_key = selected_client_name
        st.sidebar.success(f"Editing: {client_key}")

    # Load Client Data
    data = wm.load_data(client_key)
    budget = data["budget"]
    progress = wm.get_daily_progress(client_key)

    # --- Settings & Report Generator inside Sidebar ---
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📄 Reports & Settings")
    
    if st.sidebar.button("🖨️ Generate PDF Report"):
        try:
            import pdf_generator
            importlib.reload(pdf_generator)
            with st.sidebar.spinner("Generating..."):
                report_path = pdf_generator.create_wealth_report(client_key, data, progress)
                st.session_state['latest_report'] = report_path
                st.sidebar.success("Report Generated!")
                st.rerun()
        except Exception as e:
            st.sidebar.error(f"Error generating PDF: {e}")

    if 'latest_report' in st.session_state and os.path.exists(st.session_state['latest_report']):
        with open(st.session_state['latest_report'], "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Download PDF Report",
                data=f,
                file_name=os.path.basename(st.session_state['latest_report']),
                mime="application/pdf",
                use_container_width=True
            )
            
    if selected_client_name != "My Personal Plan":
        if st.sidebar.button("🗑️ Delete Profile", type="secondary"):
            st.sidebar.error("Protected for safety.")

    # --- Reminders Overdue Check & Banner ---
    if rm:
        try:
            today = datetime.now().date()
            active_reminders = rm.get_reminders(include_completed=False)
            overdue_reminders = []
            for r in active_reminders:
                due_date = datetime.fromisoformat(r["due_date"]).date()
                if due_date < today:
                    overdue_reminders.append(r)
            
            if overdue_reminders:
                overdue_count = len(overdue_reminders)
                st.markdown(f"""
                <div class="overdue-banner">
                    <h4 style="margin: 0 0 5px 0; color: #FF6B6B;">🚨 Attention: {overdue_count} Overdue Bill{'s' if overdue_count > 1 else ''} / Reminder{'s' if overdue_count > 1 else ''}!</h4>
                    <p style="margin: 0; color: #E8F5E9; font-size: 0.9rem;">
                        Please click the <b>Reminders</b> card below to complete outstanding items.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        except Exception as e:
            pass

    # --- View State Router ---
    if "active_view" not in st.session_state:
        st.session_state.active_view = "Dashboard"

    # Render Navigation Header on Sub-pages
    if st.session_state.active_view != "Dashboard":
        c_back, c_title = st.columns([1, 4])
        with c_back:
            if st.button("← Back to Cockpit", use_container_width=True):
                st.session_state.active_view = "Dashboard"
                st.rerun()
        with c_title:
            st.title(f"💰 {st.session_state.active_view}")
        st.divider()

    # --- VIEW: Dashboard Cockpit ---
    if st.session_state.active_view == "Dashboard":
        st.title(f"💰 Wealth Engine Cockpit")
        st.caption(f"Profile: {selected_client_name} | Target: ${budget['daily_target']:.2f}/day")
        st.write("")

        # 1. Main Cockpit Row: Side-by-side Progress and History
        col_left, col_right = st.columns([2, 3])
        
        with col_left:
            percent = progress['percent']
            stroke_dashoffset = 471.24 * (1.0 - (percent / 100.0))
            
            st.markdown(f"""
            <div style="background: rgba(26, 47, 26, 0.25); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 24px; height: 100%; box-sizing: border-box; backdrop-filter: blur(12px); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <h4 style="margin: 0 0 16px 0; color: #88A888; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; text-align: center;">Daily Progress</h4>
                <div style="position: relative; display: flex; align-items: center; justify-content: center; width: 170px; height: 170px;">
                    <svg width="170" height="170" viewBox="0 0 170 170" style="transform: rotate(-90deg); width: 170px; height: 170px;">
                        <circle cx="85" cy="85" r="75" stroke="rgba(255, 255, 255, 0.04)" stroke-width="12" fill="transparent" />
                        <circle cx="85" cy="85" r="75" stroke="#00FF88" stroke-width="12" fill="transparent" 
                                stroke-dasharray="471.24" stroke-dashoffset="{stroke_dashoffset}" stroke-linecap="round"
                                style="filter: drop-shadow(0 0 6px rgba(0, 255, 136, 0.6));" />
                    </svg>
                    <div style="position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                        <span style="font-size: 2.2rem; font-weight: 700; color: #E8F5E9; font-family: 'Outfit', sans-serif;">{percent}%</span>
                        <span style="font-size: 0.75rem; color: #88a888; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em; margin-top: -3px;">Completed</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if progress['percent'] >= 100:
                if 'balloons_triggered' not in st.session_state:
                    st.session_state['balloons_triggered'] = True
                    st.balloons()

        with col_right:
            df = pd.DataFrame(data["daily_log"])
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("timestamp", ascending=False)
                
                # Styled Bar Chart
                chart = alt.Chart(df).mark_bar(
                    cornerRadiusTopLeft=4,
                    cornerRadiusTopRight=4
                ).encode(
                    x=alt.X('date:T', title='Date'),
                    y=alt.Y('amount:Q', title='Amount ($)'),
                    color=alt.Color('source:N', scale=alt.Scale(range=['#00FF88', '#764BA2', '#00B36B', '#667EEA', '#E8F5E9'])),
                    tooltip=['date', 'source', 'amount']
                ).configure_view(
                    strokeWidth=0
                ).configure_axis(
                    labelColor='#88A888',
                    titleColor='#88A888',
                    gridColor='rgba(255, 255, 255, 0.05)'
                ).properties(height=230).interactive()
                st.altair_chart(chart, use_container_width=True)
            else:
                st.markdown("""
                <div style="background: rgba(26, 47, 26, 0.25); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 24px; height: 100%; box-sizing: border-box; backdrop-filter: blur(12px); box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); display: flex; align-items: center; justify-content: center; min-height: 230px;">
                    <p style="color: #88A888; font-weight: 600; text-align: center;">No activity history recorded yet.</p>
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        st.divider()

        # 2. Bottom Grid Navigation (4 tactile card buttons)
        st.subheader("🛠️ Cockpit Modules")
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
            if st.button("📉\n\nDebt Crusher", key="nav_debt", use_container_width=True):
                st.session_state.active_view = "Debt Crusher"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
            if st.button("💸\n\nBudget Builder", key="nav_budget", use_container_width=True):
                st.session_state.active_view = "Budget Builder"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
            if st.button("🏦\n\nNet Worth", key="nav_net_worth", use_container_width=True):
                st.session_state.active_view = "Net Worth"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c4:
            st.markdown('<div class="nav-card-container">', unsafe_allow_html=True)
            if st.button("⏰\n\nReminders", key="nav_reminders", use_container_width=True):
                st.session_state.active_view = "Reminders"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.divider()

        # 3. Cockpit Core Actions (Daily Log & History)
        c_log, c_history = st.columns([1, 2])
        
        with c_log:
            st.subheader("✍️ Log Earnings")
            with st.form("cockpit_log_earnings"):
                amount = st.number_input("Amount Earned ($)", min_value=0.0, step=10.0)
                sources = [s["name"] for s in budget["income_streams"]] + ["Other"]
                sources = list(dict.fromkeys(sources))
                source = st.selectbox("Source", sources)
                notes = st.text_input("Notes")
                submitted = st.form_submit_button("💰 Log Earnings", use_container_width=True)
                
                if submitted and amount > 0:
                    wm.log_earnings(client_key, amount, source, notes)
                    st.success("Logged successfully!")
                    st.rerun()

        with c_history:
            st.subheader("Recent Activity Log")
            df = pd.DataFrame(data["daily_log"])
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("timestamp", ascending=False)
                st.dataframe(df[["date", "source", "amount", "notes"]], use_container_width=True)
                
                st.write("")
                logs = data.get("daily_log", [])
                for entry in reversed(logs[-3:]):  # Show last 3
                    with st.expander(f"⚙️ {entry['date']} - ${entry['amount']:.2f} ({entry['source']})"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            st.write(f"**Notes:** {entry.get('notes', '-')}")
                        with ec2:
                            if st.button("🗑️ Delete", key=f"del_log_{entry['timestamp']}"):
                                wm.delete_earning_log(client_key, entry['timestamp'])
                                st.success("Entry deleted!")
                                st.rerun()
                                
                        with st.form(key=f"edit_log_{entry['timestamp']}"):
                            nem = st.number_input("Amount", value=float(entry['amount']), key=f"nem_{entry['timestamp']}")
                            nsrc = st.selectbox("Source", [s['name'] for s in budget.get('income_streams', [])], index=0, key=f"nsrc_{entry['timestamp']}")
                            nnotes = st.text_input("Notes", value=entry.get('notes', ''), key=f"nnotes_{entry['timestamp']}")
                            if st.form_submit_button("💾 Update"):
                                wm.update_earning_log(client_key, entry['timestamp'], nem, nsrc, nnotes)
                                st.success("Updated!")
                                st.rerun()
            else:
                st.info("No daily grind logged yet.")

    # --- VIEW: Debt Crusher ---
    elif st.session_state.active_view == "Debt Crusher":
        st.caption("Track and eliminate your outstanding debts")
        debts = wm.get_debts(client_key)
        
        with st.expander("➕ Add New Debt", expanded=len(debts) == 0):
            with st.form("add_debt_form", clear_on_submit=True):
                debt_name = st.text_input("Debt Name", placeholder="e.g., Car Note, Credit Card")
                d1, d2 = st.columns(2)
                with d1:
                    original_bal = st.number_input("Original Balance", min_value=0.0, step=100.0)
                with d2:
                    current_bal = st.number_input("Current Balance", min_value=0.0, step=100.0)
                d3, d4 = st.columns(2)
                with d3:
                    min_pmt = st.number_input("Min Payment", min_value=0.0, step=10.0)
                with d4:
                    rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0, step=0.1)
                
                if st.form_submit_button("💳 Add Debt", use_container_width=True):
                    if debt_name and current_bal > 0:
                        wm.add_debt(client_key, debt_name, original_bal, current_bal, min_pmt, rate)
                        st.success(f"Added: {debt_name}")
                        st.rerun()
        
        if debts:
            total_debt = sum(d.get("current_balance", 0) for d in debts)
            st.metric("💳 Total Outstanding Debt", f"${total_debt:,.2f}")
            st.write("")
            
            for debt in debts:
                with st.container():
                    original = debt.get("original_balance", debt.get("current_balance", 0))
                    current = debt.get("current_balance", 0)
                    paid_off = max(0, original - current)
                    progress_pct = (paid_off / original) if original > 0 else 1.0
                    
                    c1, c2, c3, c4 = st.columns([2, 1, 0.5, 0.5])
                    with c1:
                        st.markdown(f"**{debt.get('name', 'Unnamed Debt')}**")
                        st.progress(min(1.0, progress_pct))
                        st.caption(f"${current:,.2f} remaining of ${original:,.2f}")
                    with c2:
                        pmt_amt = st.number_input("Payment", min_value=0.0, step=10.0, key=f"pmt_{debt['id']}")
                    with c3:
                        if st.button("💸", key=f"btn_{debt['id']}", help="Log Payment"):
                            if pmt_amt > 0:
                                wm.log_debt_payment(client_key, debt["id"], pmt_amt)
                                st.success(f"Paid ${pmt_amt:.2f}!")
                                st.rerun()
                    with c4:
                        if st.button("🗑️", key=f"del_debt_{debt['id']}", help="Delete Debt"):
                            wm.delete_debt(client_key, debt["id"])
                            st.rerun()
                    
                    if current == 0:
                        st.success("🎉 PAID OFF!")
                    st.divider()
        else:
            st.info("No debts tracked currently. Add your first debt above to start crushing it! 💪")

    # --- VIEW: Budget Builder ---
    elif st.session_state.active_view == "Budget Builder":
        st.caption("Define the daily target by listing monthly bills and income streams.")
        
        bills_df = pd.DataFrame(budget.get("monthly_bills", []))
        total_monthly_bills = bills_df["amount"].sum() if not bills_df.empty else 0.0
        
        daily_survival = total_monthly_bills / 30.0
        current_target = float(budget.get("daily_target", 100.0))
        potential_monthly_earnings = current_target * 30.0
        potential_savings = potential_monthly_earnings - total_monthly_bills
        
        # Calculations Row
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("🔥 Survival Mode", f"${daily_survival:.2f}/day", help="Amount needed just to pay bills")
            if st.button("Set as Target", key="set_survival"):
                wm.update_budget(client_key, daily_survival, budget.get("monthly_bills", []), budget.get("income_streams", []))
                st.rerun()
        with c2:
            st.metric("🚀 Current Target", f"${current_target:.2f}/day")
        with c3:
            color = "normal" if potential_savings > 0 else "inverse"
            st.metric("💰 Potential Savings", f"${potential_savings:,.2f}/mo", delta="if target hit daily", delta_color=color)

        # Advanced calculators
        with st.expander("⚙️ Calculate Profit Goal"):
            st.caption("How much do you want to save per month?")
            desired_savings = st.number_input("Desired Monthly Savings", value=1000.0, step=100.0)
            required_daily = (total_monthly_bills + desired_savings) / 30.0
            st.write(f"To save **${desired_savings:,.0f}**, you need to earn **${required_daily:.2f}/day**.")
            
            if st.button(f"Set Target to ${required_daily:.2f}", key="set_profit"):
                 wm.update_budget(client_key, required_daily, budget.get("monthly_bills", []), budget.get("income_streams", []))
                 st.rerun()

        with st.form("target_form"):
             new_target = st.number_input("Manual Target Override ($)", value=current_target, step=5.0)
             if st.form_submit_button("Update Target", use_container_width=True):
                 wm.update_budget(client_key, new_target, budget.get("monthly_bills", []), budget.get("income_streams", []))
                 st.success("Target Updated!")
                 st.rerun()

        st.divider()
        
        # Donut Chart
        if not bills_df.empty:
             st.markdown("### 📊 Expense Allocations")
             base = alt.Chart(bills_df).encode(
                 theta=alt.Theta("amount:Q", stack=True)
             )
             pie = base.mark_arc(outerRadius=100, innerRadius=60, stroke='rgba(11,26,11,0.8)', strokeWidth=2).encode(
                 color=alt.Color("name:N", scale=alt.Scale(range=['#00FF88', '#764BA2', '#00B36B', '#667EEA', '#00E5FF', '#FF007F'])),
                 order=alt.Order("amount:Q", sort="descending"),
                 tooltip=["name", "amount"]
             )
             text = base.mark_text(radius=120, size=12, fontWeight='bold').encode(
                 text=alt.Text("amount:Q", format="$.0f"),
                 order=alt.Order("amount:Q", sort="descending"),
                 color=alt.value("#E8F5E9")
             )
             st.altair_chart((pie + text).configure_view(strokeWidth=0).configure_legend(
                 labelColor='#88A888',
                 titleColor='#88A888'
             ).properties(height=300), use_container_width=True)
             
        st.divider()

        # Monthly Bills
        st.markdown("### 📉 Monthly Bills List")
        with st.expander("➕ Add New Bill"):
            with st.form("add_bill", clear_on_submit=True):
                bname = st.text_input("Bill Name", placeholder="Rent")
                bamt = st.number_input("Amount", min_value=0.0, step=10.0)
                if st.form_submit_button("Add Bill", use_container_width=True):
                    if bname and bamt > 0:
                        current_bills = budget.get("monthly_bills", [])
                        current_bills.append({"name": bname, "amount": bamt})
                        wm.update_budget(client_key, budget.get("daily_target"), current_bills, budget.get("income_streams"))
                        st.rerun()

        if budget.get("monthly_bills"):
            for idx, bill in enumerate(budget["monthly_bills"]):
                c1, c2, c3, c4 = st.columns([3, 2, 0.5, 0.5])
                with c1:
                    st.write(f"**{bill['name']}**")
                with c2:
                    st.write(f"${bill['amount']:.2f}")
                with c3:
                    if st.button("✏️", key=f"edit_bill_btn_{idx}"):
                        st.session_state[f"editing_bill_{idx}"] = True
                with c4:
                    if st.button("🗑️", key=f"del_bill_{idx}"):
                        new_bills = [b for i, b in enumerate(budget["monthly_bills"]) if i != idx]
                        wm.update_budget(client_key, budget.get("daily_target"), new_bills, budget.get("income_streams"))
                        st.rerun()
                
                if st.session_state.get(f"editing_bill_{idx}", False):
                    with st.form(key=f"edit_bill_form_{idx}"):
                        ename = st.text_input("Name", value=bill['name'], key=f"ename_{idx}")
                        eamt = st.number_input("Amount", value=float(bill['amount']), step=10.0, key=f"eamt_{idx}")
                        if st.form_submit_button("💾 Update"):
                            budget["monthly_bills"][idx] = {"name": ename, "amount": eamt}
                            wm.update_budget(client_key, budget.get("daily_target"), budget["monthly_bills"], budget.get("income_streams"))
                            del st.session_state[f"editing_bill_{idx}"]
                            st.rerun()
        else:
            st.info("No bills configured.")

        st.divider()

        # Income Streams
        st.markdown("### 💰 Income Sources")
        with st.expander("➕ Add Income Source"):
            with st.form("add_stream", clear_on_submit=True):
                sname = st.text_input("Source Name", placeholder="Uber")
                if st.form_submit_button("Add Source", use_container_width=True):
                    if sname:
                        current_streams = budget.get("income_streams", [])
                        current_streams.append({"name": sname, "type": "variable"})
                        wm.update_budget(client_key, budget.get("daily_target"), budget.get("monthly_bills"), current_streams)
                        st.rerun()

        if budget.get("income_streams"):
            for idx, stream in enumerate(budget["income_streams"]):
                c1, c2, c3 = st.columns([4, 0.5, 0.5])
                with c1:
                    st.write(f"🔹 {stream['name']}")
                with c2:
                    if st.button("✏️", key=f"edit_stream_btn_{idx}"):
                        st.session_state[f"editing_stream_{idx}"] = True
                with c3:
                    if st.button("🗑️", key=f"del_stream_{idx}"):
                        new_streams = [s for i, s in enumerate(budget["income_streams"]) if i != idx]
                        wm.update_budget(client_key, budget.get("daily_target"), budget.get("monthly_bills"), new_streams)
                        st.rerun()
                
                if st.session_state.get(f"editing_stream_{idx}", False):
                    with st.form(key=f"edit_stream_form_{idx}"):
                        esname = st.text_input("Source Name", value=stream['name'], key=f"esname_{idx}")
                        if st.form_submit_button("💾 Update"):
                            budget["income_streams"][idx] = {"name": esname, "type": "variable"}
                            wm.update_budget(client_key, budget.get("daily_target"), budget.get("monthly_bills"), budget["income_streams"])
                            del st.session_state[f"editing_stream_{idx}"]
                            st.rerun()

    # --- VIEW: Net Worth ---
    elif st.session_state.active_view == "Net Worth":
        st.caption("Update asset balances and liabilities to calculate total net worth over time.")
        latest = wm.get_latest_net_worth(client_key)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Update Balance Sheet")
            with st.form("net_worth_form"):
                st.markdown("**Assets (+)**")
                cash = st.number_input("Cash / Bank", value=float(latest.get("assets", {}).get("cash", 0)), step=100.0)
                investments = st.number_input("Investments", value=float(latest.get("assets", {}).get("investments", 0)), step=100.0)
                vehicles = st.number_input("Vehicles", value=float(latest.get("assets", {}).get("vehicles", 0)), step=1000.0)
                property_val = st.number_input("Property/Equipment", value=float(latest.get("assets", {}).get("property", 0)), step=1000.0)
                
                st.markdown("**Liabilities (-)**")
                car_debt = st.number_input("Auto Loans", value=float(latest.get("debts", {}).get("auto", 0)), step=100.0)
                credit_debt = st.number_input("Credit Card Debt", value=float(latest.get("debts", {}).get("credit", 0)), step=50.0)
                other_debt = st.number_input("Other Debt", value=float(latest.get("debts", {}).get("other", 0)), step=50.0)
                
                if st.form_submit_button("💾 Save Snapshot", use_container_width=True):
                    assets = {"cash": cash, "investments": investments, "vehicles": vehicles, "property": property_val}
                    debts = {"auto": car_debt, "credit": credit_debt, "other": other_debt}
                    wm.save_net_worth_snapshot(client_key, assets, debts)
                    st.success("Net worth snapshot saved!")
                    st.rerun()
        
        with col2:
            total_assets = cash + investments + vehicles + property_val
            total_debts = car_debt + credit_debt + other_debt
            net_worth = total_assets - total_debts
            
            delta_color = "normal" if net_worth >= 0 else "inverse"
            st.metric("Total Net Worth", f"${net_worth:,.2f}", delta=f"Assets: ${total_assets:,.2f}", delta_color=delta_color)
            
            c1, c2 = st.columns(2)
            c1.metric("Assets Total", f"${total_assets:,.2f}")
            c2.metric("Liabilities Total", f"${total_debts:,.2f}")
            
            st.divider()
            
            st.markdown("### 📈 Net Worth History")
            history = wm.get_net_worth_history(client_key, limit=30)
            if history:
                hist_df = pd.DataFrame(history)
                hist_df["date"] = pd.to_datetime(hist_df["date"])
                hist_df = hist_df.sort_values("date")
                
                # Line chart
                chart = alt.Chart(hist_df).mark_area(
                    line={'color': '#00FF88', 'width': 3},
                    color=alt.Gradient(
                        gradient='linear',
                        stops=[alt.GradientStop(color='#00FF88', offset=0),
                               alt.GradientStop(color='rgba(0, 255, 136, 0.03)', offset=1)],
                        x1=1, y1=1, x2=1, y2=0
                    ),
                    point={'color': '#00FF88', 'size': 60, 'fill': '#0B1A0B', 'strokeWidth': 2}
                ).encode(
                    x=alt.X('date:T', title='Date'),
                    y=alt.Y('net_worth:Q', title='Net Worth ($)', scale=alt.Scale(zero=False)),
                    tooltip=['date', 'net_worth', 'total_assets', 'total_debts']
                ).configure_view(
                    strokeWidth=0
                ).configure_axis(
                    labelColor='#88A888',
                    titleColor='#88A888',
                    gridColor='rgba(255, 255, 255, 0.05)'
                ).properties(height=280).interactive()
                st.altair_chart(chart, use_container_width=True)
                
                st.markdown("### Snapshot Details Log")
                for snap in history:
                    with st.expander(f"{snap['date']} - Net Worth: ${snap.get('net_worth', 0):,.2f}"):
                        c1, c2, c3 = st.columns([2, 1, 1])
                        with c1:
                            st.write(f"**Assets:** ${snap.get('total_assets', 0):,.2f}")
                            st.write(f"**Debts:** ${snap.get('total_debts', 0):,.2f}")
                        with c2:
                            if st.button("✏️ Edit", key=f"edit_nw_{snap['timestamp']}"):
                                st.session_state[f"editing_nw_{snap['timestamp']}"] = True
                        with c3:
                            if st.button("🗑️ Delete", key=f"del_nw_{snap['timestamp']}"):
                                wm.delete_net_worth_snapshot(client_key, snap['timestamp'])
                                st.success("Deleted!")
                                st.rerun()
                        
                        if st.session_state.get(f"editing_nw_{snap['timestamp']}", False):
                            st.markdown("#### Edit Snapshot")
                            with st.form(key=f"edit_nw_form_{snap['timestamp']}"):
                                nc = st.number_input("Cash", value=float(snap.get('assets', {}).get('cash', 0)), key=f"nc_{snap['timestamp']}")
                                ni = st.number_input("Investments", value=float(snap.get('assets', {}).get('investments', 0)), key=f"ni_{snap['timestamp']}")
                                nv = st.number_input("Vehicles", value=float(snap.get('assets', {}).get('vehicles', 0)), key=f"nv_{snap['timestamp']}")
                                np = st.number_input("Property", value=float(snap.get('assets', {}).get('property', 0)), key=f"np_{snap['timestamp']}")
                                
                                na = st.number_input("Auto Loans", value=float(snap.get('debts', {}).get('auto', 0)), key=f"na_{snap['timestamp']}")
                                ncd = st.number_input("Credit Cards", value=float(snap.get('debts', {}).get('credit', 0)), key=f"ncd_{snap['timestamp']}")
                                nod = st.number_input("Other Debt", value=float(snap.get('debts', {}).get('other', 0)), key=f"nod_{snap['timestamp']}")
                                
                                if st.form_submit_button("Update Snapshot"):
                                    new_assets = {"cash": nc, "investments": ni, "vehicles": nv, "property": np}
                                    new_debts = {"auto": na, "credit": ncd, "other": nod}
                                    wm.update_net_worth_snapshot(client_key, snap['timestamp'], new_assets, new_debts)
                                    st.session_state[f"editing_nw_{snap['timestamp']}"] = False
                                    st.success("Updated!")
                                    st.rerun()
            else:
                st.info("Log your first Net Worth snapshot to begin.")

    # --- VIEW: Savings Goals ---
    elif st.session_state.active_view == "Savings Goals":
        st.caption("Create and track financial target goals.")
        goals = wm.get_savings_goals(client_key)
        
        with st.expander("➕ Add New Goal", expanded=len(goals) == 0):
            with st.form("add_goal_form", clear_on_submit=True):
                goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, New Truck")
                g1, g2 = st.columns(2)
                with g1:
                    target = st.number_input("Target Amount", min_value=0.0, step=100.0)
                with g2:
                    current = st.number_input("Already Saved", min_value=0.0, step=10.0)
                
                if st.form_submit_button("🎯 Add Goal", use_container_width=True):
                    if goal_name and target > 0:
                        wm.add_savings_goal(client_key, goal_name, target, current)
                        st.success(f"Goal created: {goal_name}")
                        st.rerun()
        
        if goals:
            total_saved = sum(g.get("current_amount", 0) for g in goals)
            total_target = sum(g.get("target_amount", 0) for g in goals)
            st.metric("💰 Total Savings Stacked", f"${total_saved:,.2f}", delta=f"Target: ${total_target:,.2f}")
            st.write("")
            
            for goal in goals:
                with st.container():
                    target_amt = goal.get("target_amount", 0)
                    current_amt = goal.get("current_amount", 0)
                    progress_pct = (current_amt / target_amt) if target_amt > 0 else 0
                    
                    c1, c2, c3, c4 = st.columns([2, 1, 0.5, 0.5])
                    with c1:
                        st.markdown(f"**{goal.get('name', 'Unnamed Goal')}**")
                        st.progress(min(1.0, progress_pct))
                        st.caption(f"${current_amt:,.2f} of ${target_amt:,.2f} ({progress_pct*100:.1f}%)")
                    with c2:
                        contrib_amt = st.number_input("Contribution Amount", min_value=0.0, step=10.0, key=f"contrib_{goal['id']}")
                    with c3:
                        if st.button("💰", key=f"goal_btn_{goal['id']}", help="Contribute"):
                            if contrib_amt > 0:
                                wm.contribute_to_goal(client_key, goal["id"], contrib_amt)
                                st.success(f"Contributed ${contrib_amt:.2f}!")
                                st.rerun()
                    with c4:
                        if st.button("🗑️", key=f"del_goal_{goal['id']}", help="Delete Goal"):
                            wm.delete_savings_goal(client_key, goal["id"])
                            st.rerun()
                    
                    if current_amt >= target_amt:
                        st.success("🎉 GOAL REACHED!")
                    st.divider()
        else:
            st.info("No active savings goals. Create one above to get started!")

    # --- VIEW: Reminders ---
    elif st.session_state.active_view == "Reminders":
        st.caption("Manage outstanding bills, renewals, inspections, and tasks")
        
        if rm is None:
            st.error("Reminders manager not loaded.")
        else:
            rtab1, rtab2, rtab3, rtab4 = st.tabs(["📅 Upcoming", "💰 Bills", "➕ Add New", "📊 All Reminders"])
            
            with rtab1:
                st.subheader("📅 Upcoming Deadlines")
                upcoming = rm.get_due_reminders(days_ahead=14)
                
                if not upcoming:
                    st.success("🎉 No upcoming deadlines! You're all caught up.")
                else:
                    today = datetime.now().date()
                    for r in upcoming:
                        due_date = datetime.fromisoformat(r["due_date"]).date()
                        days_diff = (due_date - today).days
                        
                        if days_diff < 0:
                            card_class = "reminder-overdue"
                            badge = "🔴 OVERDUE"
                        elif days_diff <= 2:
                            card_class = "reminder-due-soon"
                            badge = "🟡 DUE SOON"
                        else:
                            card_class = "reminder-upcoming"
                            badge = "🟢 Upcoming"
                        
                        st.markdown(f"""
                        <div class="{card_class}">
                            <h4 style="margin: 0; color: #E8F5E9;">{badge} | {r['title']}</h4>
                            <p style="margin: 4px 0 0 0; color: #88A888; font-size: 0.85rem;">
                                Due: {due_date.strftime('%b %d, %Y')} | Category: {r['category'].title()}
                                {f" | Amount: <b>${r['amount']:.2f}</b>" if r.get('amount') else ""}
                                {" | 🤖 Auto-Pay" if r.get('auto_pay') else ""}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns([1, 1])
                        with col_a:
                            if st.button("✅ Done", key=f"wealth_done_{r['id']}"):
                                rm.mark_complete(r["id"])
                                st.success("Completed!")
                                st.rerun()
                        with col_b:
                            if st.button("🗑️ Delete", key=f"wealth_del_{r['id']}"):
                                rm.delete_reminder(r["id"])
                                st.success("Deleted!")
                                st.rerun()
                        st.divider()

            with rtab2:
                st.subheader("💰 Bill Management")
                bills = rm.get_reminders(category="bills")
                
                if not bills:
                    st.info("No bills tracked yet. Add your first bill in the '➕ Add New' tab!")
                else:
                    total_monthly = rm.get_monthly_bills_total()
                    autopay_bills = [b for b in bills if b.get("auto_pay")]
                    manual_bills = [b for b in bills if not b.get("auto_pay")]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Monthly Bills", f"${total_monthly:,.2f}")
                    with col2:
                        st.metric("Auto-Pay Bills", len(autopay_bills))
                    with col3:
                        st.metric("Manual Pay Bills", len(manual_bills))
                    
                    st.divider()
                    
                    for b in bills:
                        with st.expander(f"💰 {b['title']} - ${b.get('amount', 0):,.2f}" + (" 🤖" if b.get("auto_pay") else "")):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Due Date:** {datetime.fromisoformat(b['due_date']).strftime('%b %d, %Y')}")
                                st.write(f"**Amount:** ${b.get('amount', 0):,.2f}")
                                st.write(f"**Recurring:** {b.get('recurring', 'One-time').title()}")
                                st.write(f"**Auto-Pay:** {'Yes 🤖' if b.get('auto_pay') else 'No'}")
                            with col2:
                                if b.get("payee"):
                                    st.write(f"**Payee:** {b.get('payee')}")
                                if b.get("account"):
                                    st.write(f"**Account:** {b.get('account')}")
                                if b.get("notes"):
                                    st.write(f"**Notes:** {b.get('notes')}")
                            
                            if b.get("payment_history"):
                                st.subheader("Payment History")
                                for p in b["payment_history"][-5:]:
                                    st.caption(f"✅ ${p['amount']:,.2f} paid on {datetime.fromisoformat(p['paid_at']).strftime('%b %d, %Y')}")
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button(f"✅ Mark Paid", key=f"wealth_paid_{b['id']}"):
                                    rm.mark_complete(b["id"])
                                    st.success("Marked paid!")
                                    st.rerun()
                            with col_b:
                                if st.button(f"🗑️ Delete Bill", key=f"wealth_delbill_{b['id']}"):
                                    rm.delete_reminder(b["id"])
                                    st.success("Deleted!")
                                    st.rerun()

            with rtab3:
                st.subheader("➕ Add New Reminder / Bill")
                with st.form("wealth_add_reminder"):
                    col1, col2 = st.columns(2)
                    with col1:
                        title = st.text_input("Title *", placeholder="Electric Bill", key="w_add_title")
                        category = st.selectbox("Category *", ["bills", "renewals", "inspections", "personal"], key="w_add_cat")
                        due_date = st.date_input("Due Date *", value=datetime.now() + timedelta(days=7), key="w_add_due_date")
                        due_time = st.time_input("Due Time (optional)", value=None, key="w_add_due_time")
                        recurring = st.selectbox("Recurring", [None, "weekly", "monthly", "yearly"], key="w_add_rec")
                    with col2:
                        amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f", key="w_add_amt")
                        payee = st.text_input("Payee", placeholder="Duke Energy", key="w_add_payee")
                        account = st.text_input("Account #", placeholder="123-456-789", key="w_add_acc")
                        auto_pay = st.checkbox("This is on Auto-Pay (just tracking)", key="w_add_auto")
                        notes = st.text_area("Notes", placeholder="Payment portal: duke-energy.com", key="w_add_notes")
                    
                    submitted = st.form_submit_button("➕ Add Reminder", use_container_width=True)
                    if submitted:
                        if not title:
                            st.error("Title is required!")
                        else:
                            if due_time:
                                full_due = datetime.combine(due_date, due_time)
                            else:
                                full_due = datetime.combine(due_date, datetime.min.time())
                            
                            rm.add_reminder(
                                title=title,
                                due_date=full_due,
                                category=category,
                                recurring=recurring,
                                amount=amount if amount > 0 else None,
                                payee=payee if payee else None,
                                account=account if account else None,
                                notes=notes if notes else None,
                                auto_pay=auto_pay
                            )
                            st.success(f"✅ Added: {title}")
                            st.rerun()

            with rtab4:
                st.subheader("📊 All Reminders")
                col1, col2 = st.columns(2)
                with col1:
                    filter_category = st.selectbox("Filter by Category", ["All", "bills", "renewals", "inspections", "personal"], key="w_filter_cat")
                with col2:
                    show_completed = st.checkbox("Show Completed", key="w_show_comp")
                
                cat = filter_category if filter_category != "All" else None
                reminders = rm.get_reminders(include_completed=show_completed, category=cat)
                
                if not reminders:
                    st.info("No reminders found with current filters.")
                else:
                    for r in reminders:
                        due_date = datetime.fromisoformat(r["due_date"])
                        status_str = "✅ Completed" if r.get("completed") else "⏳ Active"
                        amount_str = f"${r.get('amount', 0):,.2f}" if r.get("amount") else "-"
                        
                        col_a, col_b, col_c, col_d, col_e = st.columns([3, 1, 1, 1, 1])
                        with col_a:
                            st.write(f"**{r['title']}**")
                        with col_b:
                            st.write(r["category"].title())
                        with col_c:
                            st.write(due_date.strftime("%m/%d/%y"))
                        with col_d:
                            st.write(amount_str)
                        with col_e:
                            if not r.get("completed"):
                                if st.button("✅ Done", key=f"wealth_all_done_{r['id']}"):
                                    rm.mark_complete(r["id"])
                                    st.success("Completed!")
                                    st.rerun()
                        st.divider()

if __name__ == "__main__":
    st.set_page_config(page_title="Wealth Manager", page_icon="💰", layout="wide")
    main()
