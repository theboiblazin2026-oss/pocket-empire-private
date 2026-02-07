import streamlit as st
import webbrowser

st.set_page_config(
    page_title="🚀 Pocket Empire Hub",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Pocket Empire Launchpad")
st.caption("Your Central Command for Trucking, Wealth, and Automation")

# --- STATUS INDICATORS ---
# (Could be expanded to check PIDs in future)

# --- THE APPS ---
st.header("🏢 Business & Operations")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**🚛 Lead Puller**")
    st.caption("Auto-Emailer & Hunter")
    st.link_button("🚀 Launch (8507)", "http://localhost:8507", use_container_width=True)

with col2:
    st.info("**💰 Rate Negotiator**")
    st.caption("Scripts & Lane History")
    st.link_button("🚀 Launch (8508)", "http://localhost:8508", use_container_width=True)

with col3:
    st.info("**🛣️ Route Planner**")
    st.caption("Maps & Fuel Costs")
    st.link_button("🚀 Launch (8506)", "http://localhost:8506", use_container_width=True)

with col4:
    st.info("**📄 Invoices**")
    st.caption("Billing & Tracking")
    st.link_button("🚀 Launch (8504)", "http://localhost:8504", use_container_width=True)

st.divider()
st.header("🛡️ Finance & Compliance")
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.success("**💸 Wealth Manager**")
    st.caption("Net Worth & Budget")
    st.link_button("🚀 Launch (8501)", "http://localhost:8501", use_container_width=True)

with col6:
    st.success("**💳 Credit Repair**")
    st.caption("Disputes & Letters")
    st.link_button("🚀 Launch (8503)", "http://localhost:8503", use_container_width=True)

with col7:
    st.warning("**⚠️ Compliance**")
    st.caption("Driver Files & Safety")
    st.link_button("🚀 Launch (8509)", "http://localhost:8509", use_container_width=True)

with col8:
    st.secondary("**📰 News Curator**")
    st.caption("Industry Intel")
    st.link_button("🚀 Launch (8505)", "http://localhost:8505", use_container_width=True)

st.divider()
st.header("⚙️ System Status")
st.write("To restart the system, run `sh start_system.sh` in your terminal.")

# Reminder Bot Link (8502)
st.sidebar.header("🔔 Reminders")
st.sidebar.link_button("View Reminders (8502)", "http://localhost:8502")
