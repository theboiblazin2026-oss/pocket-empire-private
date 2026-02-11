import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, date

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

try:
    from pocket_transport import load_manager as lm
except ImportError:
    st.error("Pocket Transport module not found. Please verify installation.")
    st.stop()

st.set_page_config(
    page_title="Dispatch Board",
    page_icon="🚚",
    layout="wide"
)

# --- HEADER ---
st.title("🚚 Dispatch Command Center")
st.caption("Manage your loads, track revenue, and keep rolling.")

revenue = lm.get_weekly_revenue()

# --- METRICS ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Booked (Not Rolling)", f"${revenue['booked']:,.0f}")
c2.metric("Rolling (In Transit)", f"${revenue['rolling']:,.0f}")
c3.metric("Delivered (Unpaid)", f"${revenue['delivered']:,.0f}")
c4.metric("Paid (Total)", f"${revenue['paid']:,.0f}")

st.divider()

# --- NEW LOAD FORM ---
with st.expander("➕ Book New Load", expanded=False):
    with st.form("new_load_form"):
        c1, c2, c3 = st.columns(3)
        broker = c1.text_input("Broker Name", placeholder="e.g. TQL, CH Robinson")
        rate = c2.number_input("Rate ($)", min_value=0.0, step=50.0)
        commodity = c3.text_input("Commodity", placeholder="e.g. Frozen Chicken")
        
        c4, c5 = st.columns(2)
        origin = c4.text_input("Origin (City, ST)", placeholder="Atlanta, GA")
        destination = c5.text_input("Destination (City, ST)", placeholder="Chicago, IL")
        
        c6, c7 = st.columns(2)
        pick_date = c6.date_input("Pickup Date", date.today())
        drop_date = c7.date_input("Delivery Date", date.today())
        
        submitted = st.form_submit_button("✅ Book Load")
        
        if submitted:
            if broker and origin and destination and rate > 0:
                lm.create_load(
                    broker, origin, destination, rate, pick_date, drop_date, commodity=commodity
                )
                st.success(f"Load booked: {origin} -> {destination} for ${rate}")
                st.rerun()
            else:
                st.error("Please fill in Broker, Origin, Destination, and Rate.")

# --- DISPATCH BOARD (KANBAN) ---
loads = lm.load_all_loads()

if not loads:
    st.info("No loads tracked yet. Book your first load above!")
else:
    # Filter/Sort
    filter_status = st.multiselect("Filter by Status", lm.LOAD_STATUSES, default=[s for s in lm.LOAD_STATUSES if s not in ["Paid", "Cancelled"]])
    
    # Kanban Columns logic? Or just grouped lists?
    # Let's do a clean list view with status actions
    
    for load in reversed(loads):
        if filter_status and load["status"] not in filter_status:
            continue
            
        with st.container(border=True):
            cols = st.columns([0.5, 2, 1, 1, 2])
            
            # Status Indicator
            status_color = "gray"
            if load["status"] == "Booked": status_color = "blue"
            elif load["status"] in ["In Transit", "Dispatched"]: status_color = "orange"
            elif load["status"] == "Delivered": status_color = "green"
            elif load["status"] == "Paid": status_color = "gold"
            
            cols[0].markdown(f":{status_color}[**{load['status']}**]")
            
            # Route
            cols[1].markdown(f"**{load['origin']} ➝ {load['destination']}**")
            cols[1].caption(f"{load['broker']} • {load['commodity']}")
            
            # Dates
            cols[2].text(f"Pick: {load['pickup_date']}")
            cols[2].text(f"Drop: {load['delivery_date']}")
            
            # Rate
            cols[3].markdown(f"**${load['rate']:,.2f}**")
            
            # Actions
            with cols[4]:
                current_idx = lm.LOAD_STATUSES.index(load["status"])
                next_statuses = []
                if current_idx + 1 < len(lm.LOAD_STATUSES):
                   next_statuses.append(lm.LOAD_STATUSES[current_idx + 1])
                
                # Custom Status select
                new_status = st.selectbox("Update Status", lm.LOAD_STATUSES, index=current_idx, key=f"status_{load['id']}")
                
                if new_status != load["status"]:
                    lm.update_load_status(load["id"], new_status)
                    st.rerun()
                    
                if st.button("🗑️", key=f"del_{load['id']}"):
                    lm.delete_load(load['id'])
                    st.rerun()
