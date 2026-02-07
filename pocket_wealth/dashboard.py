import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import wealth_manager as wm
import client_manager as cm
import altair as alt

def main():
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

    # --- Main Dashboard ---
    st.title(f"💰 Wealth Manager: {selected_client_name}")
    st.caption(f"Target: ${budget['daily_target']:.2f}/day")

    # Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Earned Today", f"${progress['earned']:.2f}", delta=f"${progress['earned'] - progress['target']:.2f}")
    with col2:
        st.metric("Today's Target", f"${progress['target']:.2f}")
    with col3:
        color = "normal" if progress['remaining'] == 0 else "off"
        st.metric("Left to Earn", f"${progress['remaining']:.2f}", delta_color=color)
    with col4:
        total_logged = sum(e["amount"] for e in data["daily_log"])
        st.metric("Total Stacked", f"${total_logged:,.2f}")

    # Progress Bar
    st.progress(progress['percent'] / 100)
    if progress['percent'] >= 100:
        st.balloons()

    # --- Tabs ---
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Daily Grind", "💸 Budget Builder", "🔮 The Future", "⚙️ Client Settings"])

    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader("Log Earnings")
            with st.form("log_earnings"):
                amount = st.number_input("Amount Earned ($)", min_value=0.0, step=10.0)
                
                # Dynamic sources
                sources = [s["name"] for s in budget["income_streams"]] + ["Other"]
                source = st.selectbox("Source", sources)
                
                notes = st.text_input("Notes")
                submitted = st.form_submit_button("💰 Log Earnings")
                
                if submitted and amount > 0:
                    wm.log_earnings(client_key, amount, source, notes)
                    st.success("Logged!")
                    st.rerun()

        with col2:
            st.subheader("Recent Activity")
            df = pd.DataFrame(data["daily_log"])
            if not df.empty:
                df["date"] = pd.to_datetime(df["date"])
                df = df.sort_values("timestamp", ascending=False)
                st.dataframe(df[["date", "source", "amount", "notes"]], use_container_width=True)
                
                # Chart
                chart = alt.Chart(df).mark_bar().encode(
                    x='date:T',
                    y='amount:Q',
                    color='source:N',
                    tooltip=['date', 'source', 'amount']
                ).interactive()
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("No earnings logged yet.")

    with tab2:
        st.subheader("💸 Build the Budget")
        st.caption("Define the daily target by listing monthly bills.")
        
        with st.form("budget_form"):
            # Daily Target
            new_target = st.number_input("Daily Income Target ($)", value=float(budget.get("daily_target", 100.0)), step=5.0)
            
            # Bills Editor (Simple Text Area for JSON-ish entry or just list)
            st.markdown("### Monthly Bills")
            st.caption("Format: Name, Amount (one per line)")
            
            current_bills_text = ""
            for b in budget.get("monthly_bills", []):
                current_bills_text += f"{b['name']}, {b['amount']}\n"
                
            bills_input = st.text_area("Bills List", value=current_bills_text, height=150)
            
            # Income Streams
            st.markdown("### Income Streams")
            st.caption("Add Gig Apps or Jobs here (comma separated)")
            current_streams = ", ".join([s["name"] for s in budget.get("income_streams", [])])
            streams_input = st.text_input("Income Sources", value=current_streams)
            
            if st.form_submit_button("💾 Save Budget"):
                # Parse Bills
                new_bills = []
                for line in bills_input.split('\n'):
                    if ',' in line:
                        parts = line.split(',')
                        try:
                            new_bills.append({"name": parts[0].strip(), "amount": float(parts[1].strip())})
                        except:
                            pass
                
                # Parse Streams
                new_streams = [{"name": s.strip(), "target": 0} for s in streams_input.split(',') if s.strip()]
                
                wm.update_budget(client_key, new_target, new_bills, new_streams)
                st.success("Budget Updated!")
                st.rerun()

        # Visualization
        if budget.get("monthly_bills"):
            st.divider()
            bills_df = pd.DataFrame(budget["monthly_bills"])
            total_bills = bills_df["amount"].sum()
            
            c1, c2 = st.columns(2)
            c1.metric("Total Monthly Bills", f"${total_bills:,.2f}")
            c2.dataframe(bills_df, use_container_width=True)

    with tab3:
        st.subheader("🚀 Financial Cockpit")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### 🏦 Balance Sheet")
            with st.form("net_worth_form"):
                st.markdown("**Assets (+)**")
                cash = st.number_input("Cash / Bank", value=0.0, step=100.0)
                investments = st.number_input("Investments", value=0.0, step=100.0)
                vehicles = st.number_input("Vehicles (Value)", value=60000.0, step=1000.0)
                
                st.markdown("**Liabilities (-)**")
                car_debt = st.number_input("Car Note Balance", value=1000.0, step=50.0)
                credit_debt = st.number_input("Credit Card Debt", value=0.0, step=50.0)
                other_debt = st.number_input("Other Debt", value=0.0, step=50.0)
                
                if st.form_submit_button("Update Net Worth"):
                    # Logic to save snapshot could be added here
                    st.session_state['nw_cash'] = cash
                    st.session_state['nw_vehicles'] = vehicles
                    st.session_state['nw_debt'] = car_debt + credit_debt + other_debt
                    st.rerun()

        # Calculations
        total_assets = st.session_state.get('nw_cash', 0) + st.session_state.get('nw_vehicles', 60000)
        total_debt = st.session_state.get('nw_debt', 1000)
        net_worth = total_assets - total_debt
        
        with col2:
            # Net Worth Big Metric
            st.metric("Total Net Worth", f"${net_worth:,.2f}", delta=f"${total_assets:,.2f} Assets")
            
            st.divider()
            
            # Debt Payoff Visualizer
            st.markdown("### 📉 Debt Crusher: Car Note")
            debt_goal = 1000.0 # Initial
            current_debt = st.session_state.get('nw_debt', 1000)
            paid_off = max(0, debt_goal - current_debt)
            
            st.progress(paid_off / debt_goal if debt_goal > 0 else 1.0)
            c1, c2 = st.columns(2)
            c1.caption(f"Remaining: ${current_debt:,.2f}")
            c2.caption(f"Paid Off: ${paid_off:,.2f}")
            
            if current_debt == 0:
                st.balloons()
                st.success("🎉 DEBT FREE! Congratulations!")
                
            st.divider()
            
            # Simple Composition Chart
            perf_data = pd.DataFrame({
                "Category": ["Assets", "Liabilities", "Net Worth"],
                "Amount": [total_assets, total_debt, net_worth]
            })
            
            chart = alt.Chart(perf_data).mark_bar().encode(
                y='Category',
                x='Amount',
                color=alt.Color('Category', scale=alt.Scale(domain=['Assets', 'Liabilities', 'Net Worth'], range=['#4caf50', '#f44336', '#2196f3']))
            ).properties(height=200)
            
            st.altair_chart(chart, use_container_width=True)

    with tab4:
        if selected_client_name == "My Personal Plan":
            st.warning("Cannot delete the master profile.")
        else:
            st.subheader("Client Settings")
            if st.button("🗑️ Delete Budget Profile"):
                # Logic to delete file would go here
                st.error("Delete functionality protected for safety.")

if __name__ == "__main__":
    st.set_page_config(page_title="Wealth Manager", page_icon="💰", layout="wide")
    main()
