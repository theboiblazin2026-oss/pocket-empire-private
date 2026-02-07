import streamlit as st
import sys
import os
from datetime import datetime, timedelta

# Add parent to path for imports
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from reminder_manager import (
    load_reminders, add_reminder, update_reminder, get_reminder,
    get_reminders, get_due_reminders, get_monthly_bills_total,
    mark_complete, delete_reminder
)

def main():
    try:
        st.set_page_config(
            page_title="💰 Bill & Reminder Tracker",
            page_icon="💰",
            layout="wide"
        )
    except:
        pass

    # Custom CSS
    st.markdown("""
    <style>
        .big-number { font-size: 2.5rem; font-weight: bold; color: #FF6B6B; }
        .metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       padding: 20px; border-radius: 10px; color: white; }
        .overdue { background-color: #FFE5E5; border-left: 4px solid #FF0000; padding: 10px; margin: 5px 0; }
        .due-soon { background-color: #FFF3CD; border-left: 4px solid #FFC107; padding: 10px; margin: 5px 0; }
        .upcoming { background-color: #E8F5E9; border-left: 4px solid #4CAF50; padding: 10px; margin: 5px 0; }
    </style>
    """, unsafe_allow_html=True)

    st.title("💰 Bill & Reminder Tracker")

    # Dashboard Overview
    col1, col2, col3, col4 = st.columns(4)

    all_reminders = get_reminders()
    bills = [r for r in all_reminders if r.get("category") == "bills"]
    due_today = get_due_reminders(days_ahead=0)
    due_week = get_due_reminders(days_ahead=7)
    monthly_total = get_monthly_bills_total()

    with col1:
        st.metric("📋 Active Reminders", len(all_reminders))
    with col2:
        st.metric("💰 Monthly Bills", f"${monthly_total:,.2f}")
    with col3:
        overdue = [r for r in due_today if datetime.fromisoformat(r["due_date"]).date() < datetime.now().date()]
        st.metric("🔴 Overdue", len(overdue), delta=None if len(overdue) == 0 else f"-{len(overdue)}")
    with col4:
        st.metric("📅 Due This Week", len(due_week))

    st.divider()

    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Upcoming", "💰 Bills", "➕ Add New", "📊 All Reminders"])

    with tab1:
        st.subheader("📅 Upcoming Deadlines")
        
        upcoming = get_due_reminders(days_ahead=14)
        
        if not upcoming:
            st.success("🎉 No upcoming deadlines! You're all caught up.")
        else:
            today = datetime.now().date()
            
            for r in upcoming:
                due_date = datetime.fromisoformat(r["due_date"]).date()
                days_diff = (due_date - today).days
                
                # Determine styling
                if days_diff < 0:
                    style_class = "overdue"
                    badge = "🔴 OVERDUE"
                elif days_diff <= 2:
                    style_class = "due-soon"
                    badge = "🟡 DUE SOON"
                else:
                    style_class = "upcoming"
                    badge = "🟢 Upcoming"
                
                with st.container():
                    col_a, col_b, col_c = st.columns([3, 1, 1])
                    
                    with col_a:
                        amount_str = f" - **${r.get('amount', 0):,.2f}**" if r.get("amount") else ""
                        autopay = " 🤖 Auto-Pay" if r.get("auto_pay") else ""
                        recurring = f" (🔄 {r['recurring']})" if r.get("recurring") else ""
                        
                        st.markdown(f"**{r['title']}**{amount_str}{recurring}{autopay}")
                        st.caption(f"{badge} | Due: {due_date.strftime('%b %d, %Y')} | Category: {r['category'].title()}")
                    
                    with col_b:
                        if st.button("✅ Done", key=f"done_{r['id']}"):
                            mark_complete(r["id"])
                            st.rerun()
                    
                    with col_c:
                        if st.button("🗑️", key=f"del_{r['id']}"):
                            delete_reminder(r["id"])
                            st.rerun()
                    
                    st.divider()

    with tab2:
        st.subheader("💰 Bill Management")
        
        bills = get_reminders(category="bills")
        
        if not bills:
            st.info("No bills tracked yet. Add your first bill in the '➕ Add New' tab!")
        else:
            # Bills summary
            total_monthly = get_monthly_bills_total()
            autopay_bills = [b for b in bills if b.get("auto_pay")]
            manual_bills = [b for b in bills if not b.get("auto_pay")]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Monthly", f"${total_monthly:,.2f}")
            with col2:
                st.metric("Auto-Pay Bills", len(autopay_bills))
            with col3:
                st.metric("Manual Pay Bills", len(manual_bills))
            
            st.divider()
            
            # Bills table
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
                    
                    # Payment history
                    if b.get("payment_history"):
                        st.subheader("Payment History")
                        for p in b["payment_history"][-5:]:
                            st.caption(f"✅ ${p['amount']:,.2f} paid on {datetime.fromisoformat(p['paid_at']).strftime('%b %d, %Y')}")
                    
                    # Actions
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button(f"✅ Mark Paid", key=f"paid_{b['id']}"):
                            mark_complete(b["id"])
                            st.rerun()
                    with col_b:
                        if st.button(f"🗑️ Delete", key=f"delbill_{b['id']}"):
                            delete_reminder(b["id"])
                            st.rerun()

    with tab3:
        st.subheader("➕ Add New Reminder / Bill")
        
        with st.form("add_reminder"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Title *", placeholder="Electric Bill")
                category = st.selectbox("Category *", ["bills", "renewals", "inspections", "personal"])
                due_date = st.date_input("Due Date *", value=datetime.now() + timedelta(days=7))
                due_time = st.time_input("Due Time (optional)", value=None)
                recurring = st.selectbox("Recurring", [None, "weekly", "monthly", "yearly"])
            
            with col2:
                amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
                payee = st.text_input("Payee", placeholder="Duke Energy")
                account = st.text_input("Account #", placeholder="123-456-789")
                auto_pay = st.checkbox("This is on Auto-Pay (just tracking)")
                notes = st.text_area("Notes", placeholder="Payment portal: duke-energy.com")
            
            submitted = st.form_submit_button("➕ Add Reminder", use_container_width=True)
            
            if submitted:
                if not title:
                    st.error("Title is required!")
                else:
                    # Combine date and time
                    if due_time:
                        full_due = datetime.combine(due_date, due_time)
                    else:
                        full_due = datetime.combine(due_date, datetime.min.time())
                    
                    add_reminder(
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

    with tab4:
        st.subheader("📊 All Reminders")
        
        # Filters
        col1, col2 = st.columns(2)
        with col1:
            filter_category = st.selectbox("Filter by Category", ["All", "bills", "renewals", "inspections", "personal"])
        with col2:
            show_completed = st.checkbox("Show Completed")
        
        # Get filtered reminders
        cat = filter_category if filter_category != "All" else None
        reminders = get_reminders(include_completed=show_completed, category=cat)
        
        if not reminders:
            st.info("No reminders found with current filters.")
        else:
            for r in reminders:
                due_date = datetime.fromisoformat(r["due_date"])
                status = "✅ Completed" if r.get("completed") else "⏳ Active"
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
                        if st.button("✅", key=f"all_done_{r['id']}"):
                            mark_complete(r["id"])
                            st.rerun()
                
                st.divider()

    # Footer
    st.caption("💡 Tip: Add 'monthly', 'weekly', or 'yearly' to make bills recurring!")

if __name__ == "__main__":
    main()
