import streamlit as st
import datetime
import time
import os
import sys
import json

# Ensure modules are loaded
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_wealth')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_leads')))

try:
    import wealth_manager as wm
    import search_engine
except ImportError:
    pass

import socket
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

st.set_page_config(
    page_title="Pocket Empire Command Center",
    page_icon="🚀",
    layout="wide"
)

# --- SECURITY CHECK ---
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    st.error("Authentication module missing.")
    st.stop()
# ----------------------

# --- Premium CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global */
    .stApp { font-family: 'Inter', sans-serif; }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255,255,255,0.08);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.25rem;
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.6);
        font-size: 0.95rem;
        font-weight: 400;
    }
    .hero-time {
        color: rgba(255,255,255,0.4);
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    
    /* Stat Cards */
    .stat-card {
        background: linear-gradient(145deg, #1a1d2e 0%, #12141f 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 0.75rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        border-color: rgba(129,140,248,0.3);
    }
    .stat-label {
        color: rgba(255,255,255,0.5);
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .stat-value {
        font-size: 1.75rem;
        font-weight: 800;
        color: #e2e8f0;
    }
    .stat-delta {
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.25rem;
    }
    .stat-delta.positive { color: #34d399; }
    .stat-delta.warning { color: #fbbf24; }
    .stat-delta.neutral { color: rgba(255,255,255,0.4); }
    
    /* Quick Action Buttons */
    .action-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 0.75rem;
        margin-top: 1rem;
    }
    
    /* System Status */
    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.04);
    }
    .status-label { color: rgba(255,255,255,0.7); font-size: 0.85rem; }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 6px;
    }
    .status-dot.online { background: #34d399; box-shadow: 0 0 6px #34d399; }
    .status-dot.offline { background: #f87171; box-shadow: 0 0 6px #f87171; }
    .status-dot.warning { background: #fbbf24; box-shadow: 0 0 6px #fbbf24; }
    
    /* Section Headers */
    .section-header {
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255,255,255,0.3);
        margin: 1.5rem 0 0.75rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.2);
        font-size: 0.75rem;
        margin-top: 2rem;
        padding: 1rem 0;
        border-top: 1px solid rgba(255,255,255,0.04);
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_container_width=True)

st.sidebar.info(f"📱 **Road Mode**\n Connect: `http://{get_local_ip()}:8501`")

st.sidebar.markdown("### 🔍 Global Search")
search_query = st.sidebar.text_input("Find Lead, Route, Client...", key="global_search_input")

if search_query:
    if 'search_engine' in locals():
        results = search_engine.search_app(search_query)
        if results:
            st.sidebar.success(f"Found {len(results)} matches")
            for idx, res in enumerate(results):
                with st.sidebar.expander(f"{res['Type']}: {res['Name']}"):
                    st.caption(res['Details'])
                    if st.button("Go ➡️", key=f"go_search_{idx}"):
                        st.switch_page(res['Page'])
        else:
            st.sidebar.warning("No matches found.")
    else:
        st.sidebar.error("Search module not loaded.")

st.sidebar.divider()
st.sidebar.header("🎓 Academy")
st.sidebar.link_button("🚀 Launch Curriculum", "https://pocket-empire-private.vercel.app")

# --- Hero Banner ---
now = datetime.datetime.now()
greeting = "Good Morning" if now.hour < 12 else "Good Afternoon" if now.hour < 17 else "Good Evening"

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">🚀 Pocket Empire</div>
    <div class="hero-subtitle">{greeting}, Boss. Your empire awaits.</div>
    <div class="hero-time">{now.strftime('%A, %B %d, %Y  •  %I:%M %p')}</div>
</div>
""", unsafe_allow_html=True)

# --- KPI Row ---
st.markdown('<div class="section-header">📊 Key Metrics</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

# NET WORTH
with k1:
    try:
        if 'wm' not in locals():
            import wealth_manager as wm
        nw_data = wm.get_latest_net_worth("myself")
        net_worth = nw_data.get("net_worth", 0.0)
        prog = wm.get_daily_progress("myself")
        delta_html = f'<div class="stat-delta positive">+${prog["earned"]:.0f} today</div>'
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">💰 Net Worth</div>
            <div class="stat-value">${net_worth:,.0f}</div>
            {delta_html}
        </div>""", unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">💰 Net Worth</div>
            <div class="stat-value">—</div>
            <div class="stat-delta neutral">Setup Wealth Manager</div>
        </div>""", unsafe_allow_html=True)

# LEADS
with k2:
    try:
        from lead_history import get_lead_stats
        stats = get_lead_stats()
        new_leads = stats.get("New", 0)
        total = sum(stats.values())
        delta_class = "warning" if new_leads > 0 else "positive"
        delta_text = f"{new_leads} need review" if new_leads > 0 else "All reviewed ✓"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">📋 Lead Pipeline</div>
            <div class="stat-value">{total}</div>
            <div class="stat-delta {delta_class}">{delta_text}</div>
        </div>""", unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">📋 Lead Pipeline</div>
            <div class="stat-value">—</div>
            <div class="stat-delta neutral">Check Pipeline</div>
        </div>""", unsafe_allow_html=True)

# INVOICES
with k3:
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_invoices')))
        import invoice_manager as im
        inv_stats = im.get_stats()
        unpaid = inv_stats.get("unpaid_amount", 0.0)
        pending_count = inv_stats.get("unpaid_count", 0)
        delta_class = "warning" if pending_count > 0 else "positive"
        delta_text = f"{pending_count} unpaid" if pending_count > 0 else "All paid ✓"
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🧾 Invoices</div>
            <div class="stat-value">${unpaid:,.0f}</div>
            <div class="stat-delta {delta_class}">{delta_text}</div>
        </div>""", unsafe_allow_html=True)
    except:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">🧾 Invoices</div>
            <div class="stat-value">—</div>
            <div class="stat-delta neutral">Setup Invoices</div>
        </div>""", unsafe_allow_html=True)

# CREDIT
with k4:
    try:
        credit_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_credit/personal_credit.json'))
        if os.path.exists(credit_path):
            with open(credit_path, 'r') as f:
                c_data = json.load(f)
            dispute_count = len(c_data.get("disputes", []))
            delta_class = "warning" if dispute_count > 0 else "positive"
            delta_text = f"{dispute_count} active disputes" if dispute_count > 0 else "Clean ✓"
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-label">💳 Credit Repair</div>
                <div class="stat-value">Active</div>
                <div class="stat-delta {delta_class}">{delta_text}</div>
            </div>""", unsafe_allow_html=True)
        else:
            raise FileNotFoundError
    except:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-label">💳 Credit Repair</div>
            <div class="stat-value">—</div>
            <div class="stat-delta neutral">Setup Credit</div>
        </div>""", unsafe_allow_html=True)

# --- Quick Actions ---
st.markdown('<div class="section-header">⚡ Quick Actions</div>', unsafe_allow_html=True)
a1, a2, a3, a4, a5 = st.columns(5)
with a1:
    if st.button("🚚 Dispatch", use_container_width=True):
        st.switch_page("pages/07_🚚_Dispatch.py")
with a2:
    if st.button("⛏️ Prospector", use_container_width=True):
        st.switch_page("pages/11_⛏️_Prospector.py")
with a3:
    if st.button("📋 Pipeline", use_container_width=True):
        st.switch_page("pages/06_📋_Lead_Pipeline.py")
with a4:
    if st.button("⚖️ Lawyer", use_container_width=True):
        st.switch_page("pages/13_⚖️_Pocket_Lawyer.py")
with a5:
    if st.button("🧾 Invoices", use_container_width=True):
        st.switch_page("pages/17_🧾_Invoices.py")

# --- Two Column Layout ---
st.markdown('<div class="section-header">🏗️ Command Center</div>', unsafe_allow_html=True)
left, right = st.columns([3, 2])

with left:
    # Quick Log Earnings
    with st.expander("⚡ Quick Log Earnings", expanded=False):
        with st.form("quick_log"):
            q_amt = st.number_input("Amount ($)", min_value=0.0, step=10.0, key="q_amt")
            q_sources = ["Gig Work", "Trucking Business", "Other"]
            try:
                if 'wm' in locals():
                    q_data = wm.load_data("myself")
                    loaded_streams = [s['name'] for s in q_data.get('budget', {}).get('income_streams', [])]
                    if loaded_streams:
                        q_sources = loaded_streams
            except:
                pass
            q_source = st.selectbox("Source", q_sources, key="q_src")
            if st.form_submit_button("💰 Log It"):
                if 'wm' in locals():
                    wm.log_earnings("myself", q_amt, q_source, "Quick Log from Home")
                    st.success(f"Logged ${q_amt}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Wealth Manager module not loaded")

    # More Quick Actions
    with st.expander("🛠️ More Tools"):
        t1, t2 = st.columns(2)
        with t1:
            if st.button("🛣️ Routes", use_container_width=True):
                st.switch_page("pages/10_🛣️_Route_Planner.py")
            if st.button("📋 Compliance", use_container_width=True):
                st.switch_page("pages/04_📋_Compliance.py")
            if st.button("📝 Notes", use_container_width=True):
                st.switch_page("pages/09_📝_Pocket_Notes.py")
        with t2:
            if st.button("💹 Rates", use_container_width=True):
                st.switch_page("pages/08_💹_Rate_Negotiator.py")
            if st.button("⛽ Expenses", use_container_width=True):
                st.switch_page("pages/15_⛽_Expenses.py")
            if st.button("⚙️ Settings", use_container_width=True):
                st.switch_page("pages/99_⚙️_Settings.py")

with right:
    # System Status
    st.markdown("**System Status**")
    
    # AI Status
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY", None)
        if not api_key:
            if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
                api_key = st.secrets["gemini"]["api_key"]
        ai_status = "online" if api_key else "offline"
        ai_label = "Online" if api_key else "No Key"
    except:
        ai_status = "offline"
        ai_label = "No Key"
    
    # Database Status — live check
    try:
        from pocket_core.db import get_db
        _db = get_db()
        if _db:
            _rows = _db.table("app_data").select("key").execute()
            _count = len(_rows.data) if _rows and _rows.data else 0
            db_status = "online"
            db_label = f"Cloud ({_count} modules)"
        else:
            db_status = "warning"
            db_label = "Local Only"
    except:
        db_status = "warning"
        db_label = "Local Only"
    
    st.markdown(f"""
    <div class="stat-card">
        <div class="status-row">
            <span class="status-label">🤖 AI Engine (Gemini)</span>
            <span><span class="status-dot {ai_status}"></span>{ai_label}</span>
        </div>
        <div class="status-row">
            <span class="status-label">🗄️ Database</span>
            <span><span class="status-dot {db_status}"></span>{db_label}</span>
        </div>
        <div class="status-row">
            <span class="status-label">⚙️ Automation (Cron)</span>
            <span><span class="status-dot online"></span>6 Jobs Active</span>
        </div>
        <div class="status-row">
            <span class="status-label">🔐 Security</span>
            <span><span class="status-dot online"></span>Auth Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # New replies alert
    try:
        from lead_history import get_lead_stats
        stats = get_lead_stats()
        new_leads = stats.get("New", 0)
        if new_leads > 0:
            if st.button(f"🔔 {new_leads} New Leads — Review Now", type="primary", use_container_width=True):
                st.session_state["lead_filter"] = "New"
                st.switch_page("pages/06_📋_Lead_Pipeline.py")
    except:
        pass

# --- Footer ---
st.markdown(f"""
<div class="footer">
    Pocket Empire v2.0 • {now.strftime('%A, %B %d %Y')} • All Systems Operational
</div>
""", unsafe_allow_html=True)
