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
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Daily Grind", "💸 Budget Builder", "🏦 Net Worth", "📉 Debt Crusher", "🎯 Savings Goals", "⚙️ Settings"])

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
                
                # Detailed List with Actions
                st.markdown("### 📝 History")
                logs = data.get("daily_log", [])
                for entry in reversed(logs[-5:]):  # Show last 5, newest first
                    with st.expander(f"{entry['date']} - ${entry['amount']:.2f} ({entry['source']})"):
                        ec1, ec2 = st.columns(2)
                        with ec1:
                            st.write(f"**Notes:** {entry.get('notes', '-')}")
                        with ec2:
                            if st.button("🗑️ Delete", key=f"del_log_{entry['timestamp']}"):
                                wm.delete_earning_log(client_key, entry['timestamp'])
                                st.success("Entry deleted!")
                                st.rerun()
                                
                        # Edit Form inside expander
                        with st.form(key=f"edit_log_{entry['timestamp']}"):
                            nem = st.number_input("Amount", value=float(entry['amount']), key=f"nem_{entry['timestamp']}")
                            nsrc = st.selectbox("Source", [s['name'] for s in budget.get('income_streams', [])], index=0, key=f"nsrc_{entry['timestamp']}")
                            nnotes = st.text_input("Notes", value=entry.get('notes', ''), key=f"nnotes_{entry['timestamp']}")
                            
                            if st.form_submit_button("💾 Update"):
                                wm.update_earning_log(client_key, entry['timestamp'], nem, nsrc, nnotes)
                                st.success("Updated!")
                                st.rerun()
            else:
                st.info("No earnings logged yet.")

    with tab2:
        st.subheader("💸 Build the Budget")
        st.caption("Define the daily target by listing monthly bills.")
        
        # 1. Daily Target
        with st.form("target_form"):
            new_target = st.number_input("Daily Income Target ($)", value=float(budget.get("daily_target", 100.0)), step=5.0)
            if st.form_submit_button("Update Target"):
                wm.update_budget(client_key, new_target, budget.get("monthly_bills", []), budget.get("income_streams", []))
                st.success("Target Updated!")
                st.rerun()

        st.divider()

        # 2. Monthly Bills
        st.markdown("### 📉 Monthly Bills")
        
        # Add Bill
        with st.expander("➕ Add New Bill"):
            with st.form("add_bill"):
                bname = st.text_input("Bill Name", placeholder="Rent")
                bamt = st.number_input("Amount", min_value=0.0, step=10.0)
                if st.form_submit_button("Add Bill"):
                    if bname and bamt > 0:
                        current_bills = budget.get("monthly_bills", [])
                        current_bills.append({"name": bname, "amount": bamt})
                        wm.update_budget(client_key, budget.get("daily_target"), current_bills, budget.get("income_streams"))
                        st.rerun()

        # List Bills
        if budget.get("monthly_bills"):
            for idx, bill in enumerate(budget["monthly_bills"]):
                c1, c2, c3 = st.columns([3, 2, 1])
                with c1:
                    st.write(f"**{bill['name']}**")
                with c2:
                    st.write(f"${bill['amount']:.2f}")
                with c3:
                    if st.button("🗑️", key=f"del_bill_{idx}"):
                        new_bills = [b for i, b in enumerate(budget["monthly_bills"]) if i != idx]
                        wm.update_budget(client_key, budget.get("daily_target"), new_bills, budget.get("income_streams"))
                        st.rerun()
        else:
            st.info("No bills added.")

        st.divider()

        # 3. Income Streams
        st.markdown("### 💰 Income Streams")
        
        # Add Stream
        with st.expander("➕ Add Income Source"):
            with st.form("add_stream"):
                sname = st.text_input("Source Name", placeholder="Uber")
                if st.form_submit_button("Add Source"):
                    if sname:
                        current_streams = budget.get("income_streams", [])
                        current_streams.append({"name": sname, "type": "variable"})
                        wm.update_budget(client_key, budget.get("daily_target"), budget.get("monthly_bills"), current_streams)
                        st.rerun()

        # List Streams
        if budget.get("income_streams"):
            for idx, stream in enumerate(budget["income_streams"]):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.write(f"🔹 {stream['name']}")
                with c2:
                    if st.button("🗑️", key=f"del_stream_{idx}"):
                        new_streams = [s for i, s in enumerate(budget["income_streams"]) if i != idx]
                        wm.update_budget(client_key, budget.get("daily_target"), budget.get("monthly_bills"), new_streams)
                        st.rerun()
        else:
            st.info("No income streams added.")

        # Visualization
        if budget.get("monthly_bills"):
            st.divider()
            bills_df = pd.DataFrame(budget["monthly_bills"])
            total_bills = bills_df["amount"].sum()
            
            c1, c2 = st.columns(2)
            c1.metric("Total Monthly Bills", f"${total_bills:,.2f}")
            c2.dataframe(bills_df, use_container_width=True)

    with tab3:
        st.subheader("🏦 Net Worth Tracker")
        
        # Load latest snapshot
        latest = wm.get_latest_net_worth(client_key)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Update Balance Sheet")
            with st.form("net_worth_form"):
                st.markdown("**Assets (+)**")
                cash = st.number_input("Cash / Bank", value=float(latest.get("assets", {}).get("cash", 0)), step=100.0)
                investments = st.number_input("Investments", value=float(latest.get("assets", {}).get("investments", 0)), step=100.0)
                vehicles = st.number_input("Vehicles (Value)", value=float(latest.get("assets", {}).get("vehicles", 0)), step=1000.0)
                property_val = st.number_input("Property/Equipment", value=float(latest.get("assets", {}).get("property", 0)), step=1000.0)
                
                st.markdown("**Liabilities (-)**")
                car_debt = st.number_input("Auto Loans", value=float(latest.get("debts", {}).get("auto", 0)), step=100.0)
                credit_debt = st.number_input("Credit Card Debt", value=float(latest.get("debts", {}).get("credit", 0)), step=50.0)
                other_debt = st.number_input("Other Debt", value=float(latest.get("debts", {}).get("other", 0)), step=50.0)
                
                if st.form_submit_button("💾 Save Snapshot"):
                    assets = {"cash": cash, "investments": investments, "vehicles": vehicles, "property": property_val}
                    debts = {"auto": car_debt, "credit": credit_debt, "other": other_debt}
                    wm.save_net_worth_snapshot(client_key, assets, debts)
                    st.success("Net worth snapshot saved!")
                    st.rerun()
        
        with col2:
            # Calculate and display net worth
            total_assets = cash + investments + vehicles + property_val
            total_debts = car_debt + credit_debt + other_debt
            net_worth = total_assets - total_debts
            
            # Big metric
            delta_color = "normal" if net_worth >= 0 else "inverse"
            st.metric("💰 Total Net Worth", f"${net_worth:,.2f}", delta=f"Assets: ${total_assets:,.2f}", delta_color=delta_color)
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Total Assets", f"${total_assets:,.2f}")
            with c2:
                st.metric("Total Debt", f"${total_debts:,.2f}")
            
            st.divider()
            
            # Net Worth History Chart
            st.markdown("### 📈 Net Worth Over Time")
            history = wm.get_net_worth_history(client_key, limit=30)
            if history:
                hist_df = pd.DataFrame(history)
                hist_df["date"] = pd.to_datetime(hist_df["date"])
                hist_df = hist_df.sort_values("date")
                
                chart = alt.Chart(hist_df).mark_line(point=True, color="#4CAF50").encode(
                    x=alt.X('date:T', title='Date'),
                    y=alt.Y('net_worth:Q', title='Net Worth ($)'),
                    tooltip=['date', 'net_worth', 'total_assets', 'total_debts']
                ).properties(height=250).interactive()
                st.altair_chart(chart, use_container_width=True)
                
                # History Management
                st.markdown("### 🗓️ Snapshot History")
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
                                st.success("Snapshot deleted!")
                                st.rerun()
                        
                        # Edit Form
                        if st.session_state.get(f"editing_nw_{snap['timestamp']}", False):
                            st.markdown("#### Edit Snapshot")
                            with st.form(key=f"edit_nw_form_{snap['timestamp']}"):
                                # Assets
                                st.caption("Assets")
                                nc = st.number_input("Cash", value=float(snap.get('assets', {}).get('cash', 0)), key=f"nc_{snap['timestamp']}")
                                ni = st.number_input("Investments", value=float(snap.get('assets', {}).get('investments', 0)), key=f"ni_{snap['timestamp']}")
                                nv = st.number_input("Vehicles", value=float(snap.get('assets', {}).get('vehicles', 0)), key=f"nv_{snap['timestamp']}")
                                np = st.number_input("Property", value=float(snap.get('assets', {}).get('property', 0)), key=f"np_{snap['timestamp']}")
                                
                                # Debts
                                st.caption("Liabilities")
                                na = st.number_input("Auto Loans", value=float(snap.get('debts', {}).get('auto', 0)), key=f"na_{snap['timestamp']}")
                                ncd = st.number_input("Credit Cards", value=float(snap.get('debts', {}).get('credit', 0)), key=f"ncd_{snap['timestamp']}")
                                nod = st.number_input("Other Debt", value=float(snap.get('debts', {}).get('other', 0)), key=f"nod_{snap['timestamp']}")
                                
                                if st.form_submit_button("ab Update Snapshot"):
                                    new_assets = {"cash": nc, "investments": ni, "vehicles": nv, "property": np}
                                    new_debts = {"auto": na, "credit": ncd, "other": nod}
                                    wm.update_net_worth_snapshot(client_key, snap['timestamp'], new_assets, new_debts)
                                    st.session_state[f"editing_nw_{snap['timestamp']}"] = False
                                    st.success("Updated!")
                                    st.rerun()
                
                st.altair_chart(chart, use_container_width=True)
            else:
                st.info("Save your first snapshot to see your progress!")
    
    with tab4:
        st.subheader("📉 Debt Crusher")
        st.caption("Track and eliminate your debts")
        
        debts = wm.get_debts(client_key)
        
        # Add Debt Form
        with st.expander("➕ Add New Debt", expanded=len(debts) == 0):
            with st.form("add_debt_form"):
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
                
                if st.form_submit_button("💳 Add Debt"):
                    if debt_name and current_bal > 0:
                        wm.add_debt(client_key, debt_name, original_bal, current_bal, min_pmt, rate)
                        st.success(f"Added: {debt_name}")
                        st.rerun()
        
        # Debt List
        if debts:
            total_debt = sum(d.get("current_balance", 0) for d in debts)
            st.metric("💳 Total Debt", f"${total_debt:,.2f}")
            
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
                        if st.button("💸", key=f"btn_{debt['id']}", help="Pay"):
                            if pmt_amt > 0:
                                wm.log_debt_payment(client_key, debt["id"], pmt_amt)
                                st.success(f"Paid ${pmt_amt:.2f}!")
                                st.rerun()
                    with c4:
                        if st.button("🗑️", key=f"del_debt_{debt['id']}", help="Delete"):
                            wm.delete_debt(client_key, debt["id"])
                            st.rerun()
                    
                    if current == 0:
                        st.success("🎉 PAID OFF!")
                    
                    st.divider()
        else:
            st.info("No debts tracked. Add your first debt above to start crushing it! 💪")
    
    with tab5:
        st.subheader("🎯 Savings Goals")
        st.caption("Build wealth one goal at a time")
        
        goals = wm.get_savings_goals(client_key)
        
        # Add Goal Form
        with st.expander("➕ Add New Goal", expanded=len(goals) == 0):
            with st.form("add_goal_form"):
                goal_name = st.text_input("Goal Name", placeholder="e.g., Emergency Fund, New Truck")
                g1, g2 = st.columns(2)
                with g1:
                    target = st.number_input("Target Amount", min_value=0.0, step=100.0)
                with g2:
                    current = st.number_input("Already Saved", min_value=0.0, step=100.0)
                
                if st.form_submit_button("🎯 Add Goal"):
                    if goal_name and target > 0:
                        wm.add_savings_goal(client_key, goal_name, target, current)
                        st.success(f"Goal created: {goal_name}")
                        st.rerun()
        
        # Goals List
        if goals:
            total_saved = sum(g.get("current_amount", 0) for g in goals)
            total_target = sum(g.get("target_amount", 0) for g in goals)
            st.metric("💰 Total Saved", f"${total_saved:,.2f}", delta=f"of ${total_target:,.2f} target")
            
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
                        contrib_amt = st.number_input("Contribute", min_value=0.0, step=10.0, key=f"contrib_{goal['id']}")
                    with c3:
                        if st.button("💰", key=f"goal_btn_{goal['id']}", help="Add"):
                            if contrib_amt > 0:
                                wm.contribute_to_goal(client_key, goal["id"], contrib_amt)
                                st.success(f"Added ${contrib_amt:.2f}!")
                                st.rerun()
                    with c4:
                        if st.button("🗑️", key=f"del_goal_{goal['id']}", help="Delete"):
                            wm.delete_savings_goal(client_key, goal["id"])
                            st.rerun()
                    
                    if current_amt >= target_amt:
                        st.balloons()
                        st.success("🎉 GOAL REACHED!")
                    
                    st.divider()
        else:
            st.info("No savings goals yet. Add your first goal to start building wealth! 🚀")

    with tab6:
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
