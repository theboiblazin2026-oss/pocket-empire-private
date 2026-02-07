import streamlit as st
import sys
import os
from datetime import datetime

# Ensure local imports
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from rate_manager import (
    add_rate_entry, get_lane_stats, get_broker_profile, 
    generate_negotiation_script, get_all_lanes, get_all_brokers, get_recent_rates
)

def main():
    try:
        st.set_page_config(
            page_title="💰 Rate Negotiator",
            page_icon="💰",
            layout="wide"
        )
    except:
        pass

    st.title("💰 Rate Negotiator")
    st.caption("Track lane rates, analyze brokers, and generate negotiation scripts")

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🤝 Negotiate", "📊 Lane Stats", "👤 Broker Profiles", "➕ Log Rate"])

    with tab1:
        st.subheader("🤝 Generate Negotiation Script")
        
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("Origin City", placeholder="Chicago, IL", key="neg_origin")
        with col2:
            destination = st.text_input("Destination City", placeholder="Miami, FL", key="neg_dest")
        
        col3, col4 = st.columns(2)
        with col3:
            offered_rate = st.number_input("Offered Rate ($)", min_value=0.0, step=50.0, key="neg_rate")
        with col4:
            miles = st.number_input("Miles (optional)", min_value=0, step=10, key="neg_miles")
        
        if st.button("📝 Generate Script", use_container_width=True):
            if origin and destination and offered_rate > 0:
                scripts = generate_negotiation_script(origin, destination, offered_rate, miles if miles > 0 else None)
                
                for script in scripts:
                    if "LOWBALL" in script["type"] or "BELOW" in script["type"]:
                        st.error(f"**{script['type']}**")
                    elif "GOOD" in script["type"]:
                        st.success(f"**{script['type']}**")
                    else:
                        st.warning(f"**{script['type']}**")
                    
                    st.info(script["message"])
                    st.code(script["script"], language=None)
                    
                    # Copy button workaround
                    st.caption("👆 Copy the script above to use in negotiations")
            else:
                st.warning("Please fill in origin, destination, and offered rate")

    with tab2:
        st.subheader("📊 Lane Statistics")
        
        # Quick lookup
        col1, col2 = st.columns(2)
        with col1:
            lookup_origin = st.text_input("Origin", key="lookup_origin")
        with col2:
            lookup_dest = st.text_input("Destination", key="lookup_dest")
        
        if st.button("🔍 Look Up Lane"):
            if lookup_origin and lookup_dest:
                stats = get_lane_stats(lookup_origin, lookup_dest)
                if stats:
                    st.success(f"## {stats['lane']}")
                    
                    cols = st.columns(4)
                    with cols[0]:
                        st.metric("Average Rate", f"${stats['avg_rate']:,.0f}")
                    with cols[1]:
                        st.metric("Rate/Mile", f"${stats['avg_rpm']:.2f}" if stats['avg_rpm'] else "N/A")
                    with cols[2]:
                        st.metric("Quotes", stats['total_quotes'])
                    with cols[3]:
                        st.metric("Accepted", f"{stats['acceptance_rate']}%")
                    
                    st.write(f"**Range:** ${stats['min_rate']:,.0f} - ${stats['max_rate']:,.0f}")
                    if stats['trend']:
                        st.write(f"**Trend:** {stats['trend']}")
                else:
                    st.info("No data for this lane yet. Log some rates first!")
        
        st.divider()
        
        # All lanes
        st.subheader("All Tracked Lanes")
        lanes = get_all_lanes()
        
        if lanes:
            for lane in lanes[:10]:
                with st.expander(f"{lane['origin']} → {lane['destination']} ({lane['quotes']} quotes)"):
                    st.write(f"**Avg Rate:** ${lane['avg_rate']:,.0f}")
                    st.write(f"**Acceptance:** {lane['accepted']}/{lane['quotes']} ({round(lane['accepted']/lane['quotes']*100, 1) if lane['quotes'] else 0}%)")
                    if lane.get('last_quoted'):
                        st.caption(f"Last quoted: {lane['last_quoted'][:10]}")
        else:
            st.info("No lanes tracked yet. Log your first rate!")

    with tab3:
        st.subheader("👤 Broker Profiles")
        
        # Broker lookup
        broker_name = st.text_input("Broker Name", key="broker_lookup")
        
        if st.button("🔍 Look Up Broker"):
            if broker_name:
                profile = get_broker_profile(broker_name)
                if profile:
                    st.write(f"## {profile['name']}")
                    st.write(f"**Rating:** {profile['rating']}")
                    
                    cols = st.columns(3)
                    with cols[0]:
                        st.metric("Total Quotes", profile['total_quotes'])
                    with cols[1]:
                        st.metric("Accepted", profile['accepted_quotes'])
                    with cols[2]:
                        st.metric("Accept Rate", f"{profile['acceptance_rate']}%")
                    
                    st.write(f"**Avg Rate:** ${profile['avg_rate']:,.0f}")
                    
                    if profile['lanes_quoted']:
                        st.write("**Lanes quoted:**")
                        for lane in profile['lanes_quoted'][:5]:
                            st.caption(f"• {lane}")
                else:
                    st.info("No data for this broker yet.")
        
        st.divider()
        
        # All brokers
        st.subheader("All Tracked Brokers")
        brokers = get_all_brokers()
        
        if brokers:
            for broker in brokers[:10]:
                accept_rate = round(broker['accepted'] / broker['quotes'] * 100, 1) if broker['quotes'] else 0
                emoji = "✅" if accept_rate >= 50 else "🟡" if accept_rate >= 25 else "🔴"
                st.write(f"{emoji} **{broker['name']}** - {broker['quotes']} quotes, {accept_rate}% accepted")
        else:
            st.info("No brokers tracked yet.")

    with tab4:
        st.subheader("➕ Log a Rate Quote")
        
        with st.form("log_rate"):
            col1, col2 = st.columns(2)
            with col1:
                log_origin = st.text_input("Origin City *", placeholder="Chicago, IL")
                log_rate = st.number_input("Rate Offered ($) *", min_value=0.0, step=50.0)
                log_broker = st.text_input("Broker Name (optional)")
            with col2:
                log_dest = st.text_input("Destination City *", placeholder="Miami, FL")
                log_miles = st.number_input("Miles", min_value=0, step=10)
                log_accepted = st.checkbox("Did you accept this rate?")
            
            log_notes = st.text_input("Notes (optional)")
            
            if st.form_submit_button("💾 Log Rate", use_container_width=True):
                if log_origin and log_dest and log_rate > 0:
                    entry = add_rate_entry(
                        origin=log_origin,
                        destination=log_dest,
                        rate=log_rate,
                        miles=log_miles if log_miles > 0 else None,
                        broker_name=log_broker if log_broker else None,
                        accepted=log_accepted,
                        notes=log_notes if log_notes else None
                    )
                    st.success(f"✅ Rate logged! ID: {entry['id']}")
                    st.balloons()
                else:
                    st.error("Please fill in origin, destination, and rate")
        
        st.divider()
        
        # Recent entries
        st.subheader("Recent Rate Entries")
        recent = get_recent_rates(10)
        
        if recent:
            for entry in reversed(recent):
                emoji = "✅" if entry.get("accepted") else "❌"
                broker = f" ({entry['broker']})" if entry.get('broker') else ""
                st.caption(f"{emoji} {entry['origin']} → {entry['destination']}{broker} - ${entry['rate']:,.0f}")
        else:
            st.info("No rates logged yet.")

    # Footer
    st.divider()
    st.caption("💡 Tip: Use `!rate Chicago Miami` in Discord for quick lane lookups, `!negotiate Chicago Miami 1800` for scripts")

if __name__ == "__main__":
    main()
