import streamlit as st
import sys
import os
from datetime import datetime

# Ensure local imports work
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from invoice_manager import (
    load_data, save_data, update_company_info, add_client, get_clients,
    create_invoice, get_invoices, mark_invoice_paid, generate_invoice_docx, get_stats
)

OUTPUT_DIR = os.path.join(DIR, "output")

def main():
    try:
        st.set_page_config(
            page_title="📄 Invoice Generator",
            page_icon="📄",
            layout="wide"
        )
    except:
        pass

    st.title("📄 Invoice Generator")
    st.caption("Create professional invoices for your trucking loads")

    # Dashboard stats
    stats = get_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Invoiced", f"${stats['total_invoiced']:,.2f}")
    with col2:
        st.metric("Paid", f"${stats['paid_amount']:,.2f}", delta=f"{stats['paid_count']} invoices")
    with col3:
        st.metric("Unpaid", f"${stats['unpaid_amount']:,.2f}", delta=f"-{stats['unpaid_count']} pending" if stats['unpaid_count'] > 0 else None)
    with col4:
        st.metric("Total Invoices", stats['total_invoices'])

    st.divider()

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["➕ Create Invoice", "📋 All Invoices", "👥 Clients", "⚙️ Settings"])

    with tab1:
        st.subheader("➕ Create New Invoice")
        
        clients = get_clients()
        
        if not clients:
            st.warning("⚠️ No clients found. Add a client in the 'Clients' tab first.")
        else:
            with st.form("create_invoice"):
                # Client selection
                client_options = {f"{c['name']} ({c['city_state_zip']})": c['id'] for c in clients}
                selected_client = st.selectbox("Select Client", options=list(client_options.keys()))
                
                st.subheader("Line Items")
                st.caption("Add the loads/services for this invoice")
                
                # Route Calculator Integration
                with st.expander("🚛 Calculate Route (Auto-fill mileage)"):
                    st.caption("Use Route Planner to calculate distance and rate")
                    rcol1, rcol2 = st.columns(2)
                    with rcol1:
                        route_origin = st.text_input("Origin City", placeholder="Chicago, IL", key="route_orig")
                    with rcol2:
                        route_dest = st.text_input("Destination City", placeholder="Miami, FL", key="route_dest")
                    
                    rate_per_mile = st.number_input("Rate per Mile ($)", value=2.50, step=0.05, key="rpm")
                    
                    if st.button("📍 Calculate Route"):
                        if route_origin and route_dest:
                            import requests
                            import urllib.parse
                            
                            url_base = "https://nominatim.openstreetmap.org/search"
                            headers = {'User-Agent': 'AntigravityAgent/1.0'}
                            
                            try:
                                r_o = requests.get(f"{url_base}?q={urllib.parse.quote(route_origin)}&format=json&limit=1", headers=headers).json()
                                r_d = requests.get(f"{url_base}?q={urllib.parse.quote(route_dest)}&format=json&limit=1", headers=headers).json()
                                
                                if r_o and r_d:
                                    o_lon, o_lat = r_o[0]['lon'], r_o[0]['lat']
                                    d_lon, d_lat = r_d[0]['lon'], r_d[0]['lat']
                                    
                                    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{o_lon},{o_lat};{d_lon},{d_lat}?overview=false"
                                    r_route = requests.get(osrm_url).json()
                                    
                                    if r_route['code'] == 'Ok':
                                        dist_meters = r_route['routes'][0]['distance']
                                        dist_miles = round(dist_meters * 0.000621371, 1)
                                        total_rate = round(dist_miles * rate_per_mile, 2)
                                        
                                        st.success(f"📏 **{dist_miles:,.1f} miles** @ ${rate_per_mile}/mi = **${total_rate:,.2f}**")
                                        st.session_state['calc_desc'] = f"Load: {route_origin} to {route_dest} ({dist_miles:,.0f} miles)"
                                        st.session_state['calc_rate'] = total_rate
                                        st.info("👆 Values saved! Use them in line item below.")
                                    else:
                                        st.error("Route calculation failed.")
                                else:
                                    st.error("Could not find one or both locations.")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        else:
                            st.warning("Enter both origin and destination.")
                
                # Dynamic line items
                num_items = st.number_input("Number of line items", min_value=1, max_value=10, value=1)
                
                line_items = []
                for i in range(int(num_items)):
                    cols = st.columns([3, 1, 1])
                    with cols[0]:
                        # Pre-fill from route calculator if available
                        default_desc = st.session_state.get('calc_desc', '') if i == 0 else ""
                        desc = st.text_input(f"Description #{i+1}", value=default_desc, key=f"desc_{i}", 
                                            placeholder="Load from Chicago to Miami - 1200 miles")
                    with cols[1]:
                        qty = st.number_input(f"Qty #{i+1}", min_value=1, value=1, key=f"qty_{i}")
                    with cols[2]:
                        # Pre-fill rate from route calculator if available
                        default_rate = st.session_state.get('calc_rate', 0.0) if i == 0 else 0.0
                        rate = st.number_input(f"Rate #{i+1}", min_value=0.0, value=float(default_rate), step=0.01, key=f"rate_{i}")
                    
                    if desc and rate > 0:
                        line_items.append({
                            "description": desc,
                            "quantity": qty,
                            "rate": rate
                        })
    
                
                # Notes and due date
                notes = st.text_area("Notes (optional)", placeholder="Payment terms, special instructions, etc.")
                due_days = st.number_input("Payment due in (days)", min_value=1, max_value=90, value=30)
                
                # Calculate total preview
                if line_items:
                    total = sum(item["quantity"] * item["rate"] for item in line_items)
                    st.info(f"**Invoice Total: ${total:,.2f}**")
                
                submitted = st.form_submit_button("📄 Create Invoice", use_container_width=True)
                
                if submitted:
                    if not line_items:
                        st.error("Please add at least one line item with a description and rate.")
                    else:
                        client_id = client_options[selected_client]
                        invoice = create_invoice(
                            client_id=client_id,
                            line_items=line_items,
                            notes=notes if notes else None,
                            due_days=due_days
                        )
                        
                        # Generate DOCX
                        filepath = generate_invoice_docx(invoice["invoice_number"])
                        
                        st.success(f"✅ Created Invoice #{invoice['invoice_number']}")
                        st.balloons()
                        
                        # Download button
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                "⬇️ Download Invoice",
                                f.read(),
                                file_name=os.path.basename(filepath),
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )

    with tab2:
        st.subheader("📋 All Invoices")
        
        # Filter
        status_filter = st.selectbox("Filter by Status", ["All", "unpaid", "paid"])
        
        invoices = get_invoices(status=None if status_filter == "All" else status_filter)
        
        if not invoices:
            st.info("No invoices found.")
        else:
            for inv in invoices:
                status_emoji = "✅" if inv["status"] == "paid" else "⏳"
                
                with st.expander(f"{status_emoji} Invoice #{inv['invoice_number']} - {inv['client']['name']} - ${inv['total']:,.2f}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Client:** {inv['client']['name']}")
                        st.write(f"**Date:** {datetime.fromisoformat(inv['date']).strftime('%b %d, %Y')}")
                        st.write(f"**Due:** {datetime.fromisoformat(inv['due_date']).strftime('%b %d, %Y')}")
                        st.write(f"**Status:** {inv['status'].upper()}")
                    
                    with col2:
                        st.write("**Line Items:**")
                        for item in inv["line_items"]:
                            st.caption(f"• {item['description']} - {item['quantity']} x ${item['rate']:,.2f}")
                        st.write(f"**Total: ${inv['total']:,.2f}**")
                    
                    # Actions
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if inv["status"] == "unpaid":
                            if st.button("✅ Mark Paid", key=f"paid_{inv['invoice_number']}"):
                                mark_invoice_paid(inv["invoice_number"])
                                st.rerun()
                    
                    with col_b:
                        # Generate/Download
                        filepath = os.path.join(OUTPUT_DIR, f"Invoice_{inv['invoice_number']}*.docx")
                        import glob
                        files = glob.glob(filepath)
                        if files:
                            with open(files[0], 'rb') as f:
                                st.download_button(
                                    "⬇️ Download",
                                    f.read(),
                                    file_name=os.path.basename(files[0]),
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key=f"dl_{inv['invoice_number']}"
                                )
                        else:
                            if st.button("📄 Generate", key=f"gen_{inv['invoice_number']}"):
                                generate_invoice_docx(inv["invoice_number"])
                                st.rerun()

    with tab3:
        st.subheader("👥 Client Management")
        
        # Add new client
        with st.form("add_client"):
            st.write("**Add New Client**")
            col1, col2 = st.columns(2)
            
            with col1:
                client_name = st.text_input("Company Name *")
                client_address = st.text_input("Address *")
            with col2:
                client_csz = st.text_input("City, State ZIP *")
                client_email = st.text_input("Email (optional)")
            
            if st.form_submit_button("➕ Add Client"):
                if client_name and client_address and client_csz:
                    add_client(client_name, client_address, client_csz, client_email)
                    st.success(f"✅ Added client: {client_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
        
        st.divider()
        
        # List existing clients
        st.write("**Existing Clients:**")
        clients = get_clients()
        
        if clients:
            for c in clients:
                with st.expander(f"👤 {c['name']}"):
                    st.write(f"**Address:** {c['address']}")
                    st.write(f"**City/State/ZIP:** {c['city_state_zip']}")
                    if c.get('email'):
                        st.write(f"**Email:** {c['email']}")
        else:
            st.info("No clients added yet.")

    with tab4:
        st.subheader("⚙️ Company Settings")
        
        data = load_data()
        company = data.get("company_info", {})
        
        with st.form("company_settings"):
            st.write("**Your Company Information (appears on invoices)**")
            
            comp_name = st.text_input("Company Name", value=company.get("name", ""))
            comp_address = st.text_input("Address", value=company.get("address", ""))
            comp_csz = st.text_input("City, State ZIP", value=company.get("city_state_zip", ""))
            comp_phone = st.text_input("Phone", value=company.get("phone", ""))
            comp_email = st.text_input("Email", value=company.get("email", ""))
            
            if st.form_submit_button("💾 Save Settings"):
                update_company_info(comp_name, comp_address, comp_csz, comp_phone, comp_email)
                st.success("✅ Company info saved!")
                st.rerun()

    # Footer
    st.divider()
    st.caption("💡 Tip: Add clients first, then create invoices for each load!")

if __name__ == "__main__":
    main()
