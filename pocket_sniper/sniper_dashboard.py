import streamlit as st
import pandas as pd
import json
import os
import scraper
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.json")
FINDS_FILE = os.path.join(DATA_DIR, "finds.json")

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    st.title("🎯 Deal Finder (Sniper)")
    
    # Metrics
    finds = load_json(FINDS_FILE)
    alerts = load_json(ALERTS_FILE)
    
    unread_finds = [f for f in finds if not f.get('read', False)]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Alerts", len([a for a in alerts if a.get('active', True)]))
    col2.metric("Unread Deals", len(unread_finds))
    if col3.button("🔄 Run Scan Now", type="primary"):
        with st.spinner("Scanning markets... this might take a moment..."):
            msg = scraper.run_sniper()
            st.success(msg)
            # Reload finds after scan
            finds = load_json(FINDS_FILE)
            unread_finds = [f for f in finds if not f.get('read', False)]
            st.rerun()

    tab1, tab2 = st.tabs(["🛍️ Fresh Finds", "⚙️ Manage Alerts"])
    
    with tab1:
        st.subheader("Latest Deals")
        
        filter_mode = st.radio("Show:", ["Unread Only", "All"], horizontal=True)
        display_finds = unread_finds if filter_mode == "Unread Only" else finds
        
        if not display_finds:
            st.info("No deals found yet. Check your alerts or run a scan!")
        else:
            # Group by Query? Or just list?
            for find in display_finds[:50]: # Limit display
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    c1.markdown(f"#### [{find.get('title', 'No Title')}]({find.get('link', '#')})")
                    c1.caption(f"📍 {find.get('location')} | 🕒 {find.get('found_at')}")
                    
                    c2.markdown(f"### {find.get('price')}")
                    
                    if not find.get('read'):
                        if c2.button("Mark Read", key=f"read_{find['id']}"):
                            # Update JSON
                            # We load full list, find item, update, save
                            full_list = load_json(FINDS_FILE)
                            for item in full_list:
                                if item['id'] == find['id']:
                                    item['read'] = True
                                    break
                            save_json(FINDS_FILE, full_list)
                            st.rerun()
    
    with tab2:
        st.subheader("Configure Targets")
        
        # Add New
        with st.form("add_alert"):
            c1, c2 = st.columns(2)
            keyword = c1.text_input("Keyword", placeholder="e.g. Macbook Pro M1")
            city = c2.text_input("City (subdomain)", value="newyork", help="e.g. 'sfbay' for SF, 'dallas' for Dallas")
            
            c3, c4 = st.columns(2)
            min_p = c3.number_input("Min Price", value=0)
            max_p = c4.number_input("Max Price", value=1000)
            
            if st.form_submit_button("➕ Add Alert"):
                new_alert = {
                    "id": f"{city}_{keyword}_{datetime.now().timestamp()}",
                    "keyword": keyword,
                    "city": city,
                    "min_price": min_p if min_p > 0 else None,
                    "max_price": max_p if max_p > 0 else None,
                    "active": True
                }
                alerts.append(new_alert)
                save_json(ALERTS_FILE, alerts)
                st.success(f"Tracking: {keyword}")
                st.rerun()
        
        st.divider()
        
        # List Alerts
        for i, alert in enumerate(alerts):
            c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
            c1.write(f"**{alert['keyword']}**")
            c2.write(f"📍 {alert['city']}")
            c3.write(f"${alert.get('min_price', 0)} - ${alert.get('max_price', 'Any')}")
            
            if c4.button("🗑️", key=f"del_{i}"):
                alerts.pop(i)
                save_json(ALERTS_FILE, alerts)
                st.rerun()

if __name__ == "__main__":
    st.set_page_config(page_title="Deal Finder", page_icon="🎯")
    main()
