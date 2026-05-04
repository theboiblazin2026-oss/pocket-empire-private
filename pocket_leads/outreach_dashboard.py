import os
import requests
import json
import webbrowser
from datetime import datetime
from dotenv import load_dotenv

load_dotenv("/Volumes/CeeJay SSD/Projects/lead puller/.env")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

BOUNCE_FILE = "/Users/newguy/.gemini/antigravity/brain/9f9ec288-5a66-4f35-85b5-ad773cec8808/bounced_emails.md"
REPLIES_FILE = "/Users/newguy/.gemini/antigravity/brain/9f9ec288-5a66-4f35-85b5-ad773cec8808/replies_log.json"
OPTOUTS_FILE = "/Users/newguy/.gemini/antigravity/brain/9f9ec288-5a66-4f35-85b5-ad773cec8808/opt_outs.json"
# Try custom domain first, fallback to Vercel
TRACK_DOMAIN = "track.jayboiservicesllc.com"
FALLBACK_DOMAIN = "exo-halo.vercel.app"
API_URL = f"https://{FALLBACK_DOMAIN}/api/opens"
CLICKS_API_URL = f"https://{FALLBACK_DOMAIN}/api/clicks"
HTML_OUTPUT = os.path.expanduser("~/Desktop/jayboi_outreach_dashboard.html")

# Pipeline data
TRUCK_LEADS = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/new_authorities.json"
B2B_LEADS = "/Users/newguy/.gemini/antigravity/playground/exo-halo/scripts/latest_maps_leads.json"

# New Multi-State Realtor Data Paths
FL_LEADS = "/Users/newguy/.gemini/antigravity/playground/exo-halo/scripts/fl_sos_scraper.json"
TX_LEADS = "/Users/newguy/.gemini/antigravity/playground/exo-halo/scripts/tx_sos_scraper.json"
AL_LEADS = "/Users/newguy/.gemini/antigravity/playground/exo-halo/scripts/al_sos_scraper.json"
SC_LEADS = "/Users/newguy/.gemini/antigravity/playground/exo-halo/scripts/sc_sos_scraper.json"
NC_LEADS = "/Users/newguy/.gemini/antigravity/playground/exo-halo/scripts/nc_sos_scraper.json"

TRUCK_SENT = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/truck_sent_today.txt"
B2B_SENT = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/b2b_sent_today.txt"
REALTOR_SENT = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/realtor_sent_today.txt"
LINKEDIN_SENT = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/linkedin_sent_today.txt"

LAST_RUN_FILE = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/last_run.txt"
LAST_MC_FILE = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_leads/data/last_mc.txt"
INVOICES_FILE = "/Users/newguy/.gemini/antigravity/playground/shimmering-eagle/pocket_invoices/invoices.json"
CALL_LIST_FILE = "/Users/newguy/.gemini/antigravity/brain/9f9ec288-5a66-4f35-85b5-ad773cec8808/call_hit_list.md"

def load_json_len(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return len(json.load(f))
        except: pass
    return 0

def load_file_int(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                val = f.read().strip()
                if val: return int(val)
        except: pass
    return 0

def load_file_str(filepath, default="Unknown"):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return f.read().strip()
        except: pass
    return default

def get_opens():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[-] API Error: {e}")
    return {"opens": [], "count": 0}

def get_clicks():
    try:
        response = requests.get(CLICKS_API_URL, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[-] CLICKS API Error: {e}")
    return {"clicks": [], "count": 0}

def get_revenue():
    if os.path.exists(INVOICES_FILE):
        try:
            with open(INVOICES_FILE, "r") as f:
                data = json.load(f)
                invoices = data.get("invoices", [])
                paid = [i for i in invoices if i.get("status") == "paid"]
                return sum(float(i.get("total", 0)) for i in paid)
        except Exception as e:
            print(f"[-] Revenue Error: {e}")
    return 0.0

def get_bounces():
    bounces = []
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            resp = requests.get(f"{SUPABASE_URL}/rest/v1/bounces?select=email", headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}, timeout=7)
            if resp.status_code == 200:
                bounces = [item["email"] for item in resp.json()]
        except Exception as e:
            print(f"[-] Supabase Warning: Project is likely hibernated. Please wake it up at supabase.com/dashboard")
    return bounces

def get_replies():
    replies = []
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            resp = requests.get(f"{SUPABASE_URL}/rest/v1/replies?select=sender,date,subject,snippet&order=id.desc&limit=30", headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}, timeout=7)
            if resp.status_code == 200:
                replies = resp.json()
        except:
            pass
    return replies
    
def get_optouts():
    optouts = []
    if os.path.exists(OPTOUTS_FILE):
        try:
            with open(OPTOUTS_FILE, "r") as f:
                optouts = json.load(f)
        except: pass
    return optouts

def parse_call_list():
    html_out = ""
    json_path = CALL_LIST_FILE.replace(".md", ".json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r") as f:
                data = __import__('json').load(f)
                for name, info in data.items():
                    phone = info.get("phone", "No Phone")
                    area = info.get("area", "Unknown Area")
                    date = info.get("date_added", "Unknown Date")
                    
                    html_out += f'''
                    <div class="bg-slate-800/60 rounded-xl p-4 border border-slate-700 hover:border-fuchsia-500/50 transition-colors flex flex-col justify-between">
                        <div>
                            <div class="flex justify-between items-start mb-2">
                                <div class="font-bold text-white truncate mr-2" title="{name}">{name}</div>
                                <div class="text-[10px] text-slate-400 bg-slate-900/80 px-2 py-1 rounded border border-slate-700 whitespace-nowrap">{date}</div>
                            </div>
                            <div class="text-sm font-semibold text-fuchsia-300 mb-1 flex items-center gap-2">📞 {phone}</div>
                            <div class="text-xs text-slate-400 mb-4 flex items-center gap-2 truncate">📍 {area}</div>
                        </div>
                        <select class="w-full bg-slate-900 text-slate-300 text-xs border border-slate-600 rounded-lg p-2 focus:ring-fuchsia-500 focus:border-fuchsia-500 status-dropdown transition-colors" data-lead="{name}">
                            <option value="new">🆕 New Lead</option>
                            <option value="contacted">⏳ Pending / Contacted</option>
                            <option value="sold">✅ Sold ($500 package)</option>
                            <option value="dead">❌ Dead Lead</option>
                        </select>
                    </div>
                    '''
        except Exception as e:
            print(f"[-] Error parsing JSON call list: {e}")
    return html_out

def generate_html(opens_data, clicks_data, bounces, replies, optouts, revenue):
    call_list_html = parse_call_list()
    opens = opens_data.get("opens", [])[:25]
    open_count = opens_data.get("count", 0)
    click_count = clicks_data.get("count", 0)
    last_run = "⏸️ System Paused (Awaiting First Cloud Sync...)"
    next_mc = "Auto-Pilot"
    
    truck_queue = 0
    b2b_queue = 0
    realtor_queue = 0
    
    total_queue = 0
    total_sent = 0
    truck_sent = 0
    b2b_sent = 0
    realtor_sent = 0
    linkedin_sent = 0
    
    max_sent = 50  # New unified app daily limit
    
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            resp = requests.get(f"{SUPABASE_URL}/rest/v1/pipeline_metrics", headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}, timeout=5)
            if resp.status_code == 200:
                results = resp.json()
                for r in results:
                    name = r.get("metric_name")
                    val = r.get("metric_value", 0)
                    if name == "pending":
                        total_queue = val
                        b2b_queue = val
                    elif name == "sent_today":
                        total_sent = val
                        b2b_sent = val
                    
                    if r.get("last_updated"):
                        try:
                            # Format ugly ISO back to pretty
                            dt = datetime.fromisoformat(r["last_updated"])
                            last_run = dt.strftime("%I:%M %p")
                        except: pass
        except Exception as e:
            print(f"[-] Supabase Warning: Project is likely hibernated. Please wake it up at supabase.com/dashboard")
    
    send_pct = int((total_sent / max_sent) * 100) if max_sent > 0 else 0
    
    truck_opens = sum(1 for o in opens if "MC" in o.get("campaign", "") or "Checklist" in o.get("campaign", "") or "Trucks" in o.get("campaign", ""))
    b2b_opens = sum(1 for o in opens if "B2B" in o.get("campaign", "") or "Partnership" in o.get("campaign", "") or "B2B_Core" in o.get("campaign", ""))
    realtor_opens = sum(1 for o in opens if "Realtor" in o.get("campaign", "") or "Design" in o.get("campaign", "") or "High-end" in o.get("campaign", "") or "Tech_Trap" in o.get("campaign", ""))
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jayboi Services Analytics v3.0</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #0f172a; color: #e2e8f0; }}
            .glass {{ background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
            /* Custom Scrollbar */
            ::-webkit-scrollbar {{ width: 8px; }}
            ::-webkit-scrollbar-track {{ background: #0f172a; }}
            ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #475569; }}
        </style>
    </head>
    <body class="min-h-screen p-6 font-sans">
        <div class="max-w-7xl mx-auto">
            
            <div class="flex items-center justify-between mb-8">
                <div>
                    <h1 class="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-emerald-400 to-rose-400">
                        🚀 Jayboi Outreach v3.0
                    </h1>
                    <p class="text-slate-400 mt-2 font-mono text-sm">Live System Analytics Page Generated: {datetime.now().strftime('%B %d, %Y %I:%M %p')}</p>
                    <p class="text-emerald-400 font-bold mt-1">🔄 Last Master Script Execution: {last_run}</p>
                </div>
                
                <!-- Quick Access CRM Buttons -->
                <div class="flex gap-3 flex-wrap justify-end">
                    <a href="https://supabase.com/dashboard/project/rxkypdnjaptvhyqyollk/editor" target="_blank" class="px-5 py-2.5 bg-emerald-600/90 hover:bg-emerald-500 rounded-xl text-white font-bold text-sm shadow-xl shadow-emerald-900/20 border border-emerald-500/50 transition-all hover:-translate-y-1 flex items-center gap-2">
                        <span>🟢</span> Cloud Database (Supabase)
                    </a>
                    <a href="https://mail.google.com/mail/u/info@jayboiservicesllc.com/" target="_blank" class="px-5 py-2.5 bg-blue-600/90 hover:bg-blue-500 rounded-xl text-white font-bold text-sm shadow-xl shadow-blue-900/20 border border-blue-500/50 transition-all hover:-translate-y-1 flex items-center gap-2">
                        <span>📧</span> Workspace Direct Webmail
                    </a>
                    <a href="https://vercel.com/newguy/exo-halo/analytics" target="_blank" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-700 rounded-xl text-white font-bold text-sm shadow-xl shadow-slate-900/40 border border-slate-600 transition-all hover:-translate-y-1 flex items-center gap-2">
                        <span>▲</span> Vercel DNS Analytics
                    </a>
                </div>
            </div>

            <!-- Pipeline Status Row -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <!-- Fuel Gauge v3 -->
                <div class="glass p-4 rounded-2xl shadow border-l-4 border-indigo-500 hover:border-indigo-400 transition-all flex flex-col justify-between">
                    <div>
                        <h3 class="text-slate-400 font-semibold mb-2">Omni-Channel Drop Load</h3>
                        <div class="w-full bg-slate-700/50 rounded-full h-2.5 mb-2 overflow-hidden border border-slate-600">
                            <div class="bg-indigo-500 h-full rounded-full transition-all duration-1000" style="width: {send_pct}%"></div>
                        </div>
                        <p class="text-2xl font-bold text-white tracking-tight">{total_sent} <span class="text-sm font-normal text-slate-400">/ {max_sent} Max</span></p>
                    </div>
                    <div class="grid grid-cols-2 gap-x-2 gap-y-1 mt-2 bg-slate-900/40 p-2 rounded-xl">
                        <p class="text-[11px] text-slate-400 uppercase">🚚 Truck: <span class="text-emerald-400 font-bold">{truck_sent}</span></p>
                        <p class="text-[11px] text-slate-400 uppercase">🏢 B2B: <span class="text-blue-400 font-bold">{b2b_sent}</span></p>
                        <p class="text-[11px] text-slate-400 uppercase">🏡 Realtor: <span class="text-rose-400 font-bold">{realtor_sent}</span></p>
                        <p class="text-[11px] text-slate-400 uppercase">💼 LnkdIn: <span class="text-sky-400 font-bold">{linkedin_sent}</span></p>
                    </div>
                </div>
                
                <!-- Pipeline Health -->
                <div class="glass p-5 rounded-2xl shadow border-l-4 border-fuchsia-500 hover:border-fuchsia-400 transition-all flex flex-col justify-between">
                    <div>
                        <h3 class="text-slate-400 font-semibold mb-1">Untapped Fuel Pipeline</h3>
                        <p class="text-3xl font-bold text-white tracking-tight">{total_queue} <span class="text-sm font-normal text-slate-400">waiting</span></p>
                    </div>
                    <div class="text-xs text-slate-400 flex flex-col gap-1.5 bg-slate-900/40 p-2.5 rounded-xl border border-slate-700/50 mt-2">
                        <span class="flex justify-between"><span>Search Query:</span> <strong class="text-emerald-300">Live Scrape</strong></span>
                        <span class="flex justify-between"><span>DB Status:</span> <strong class="text-rose-300">Synced</strong></span>
                    </div>
                </div>
                
                <!-- Campaign Showdown -->
                <div class="glass p-3 lg:p-5 rounded-2xl shadow border-l-4 border-amber-500 hover:border-amber-400 transition-all flex flex-col justify-between">
                    <h3 class="text-slate-400 font-semibold mb-1 text-sm lg:text-base">Campaign Dominance</h3>
                    <div class="grid grid-cols-3 divide-x divide-slate-600/50 mt-auto bg-slate-900/40 p-1.5 lg:p-3 rounded-xl border border-slate-700/50">
                        <div class="text-center flex flex-col items-center justify-center">
                            <p class="text-lg lg:text-2xl font-black text-emerald-400 drop-shadow-md leading-none mb-1">{truck_opens}</p>
                            <p class="text-[8px] lg:text-[10px] uppercase font-semibold text-slate-400">Trucks</p>
                        </div>
                        <div class="text-center flex flex-col items-center justify-center">
                            <p class="text-lg lg:text-2xl font-black text-blue-400 drop-shadow-md leading-none mb-1">{b2b_opens}</p>
                            <p class="text-[8px] lg:text-[10px] uppercase font-semibold text-slate-400">B2B Core</p>
                        </div>
                        <div class="text-center flex flex-col items-center justify-center relative">
                            <div class="absolute -top-3 left-0 right-0 flex justify-center w-full">
                                <span class="text-[7px] bg-rose-500 text-white px-1 leading-tight rounded shadow">NEW</span>
                            </div>
                            <p class="text-lg lg:text-2xl font-black text-rose-400 drop-shadow-md leading-none mb-1">{realtor_opens}</p>
                            <p class="text-[7px] lg:text-[10px] uppercase font-semibold text-slate-400 w-full truncate px-0.5">Realtors</p>
                        </div>
                    </div>
                </div>
                
                <!-- Opt-Outs / Bounce -->
                <div class="glass p-5 rounded-2xl shadow border-l-4 border-rose-500 hover:border-rose-400 transition-all">
                    <h3 class="text-slate-400 font-semibold mb-1">Reputation Shield</h3>
                    <div class="mt-4 flex flex-col gap-3">
                        <div class="flex items-center justify-between bg-rose-950/30 p-2 rounded-lg border border-rose-900/50">
                            <span class="text-xs text-rose-200 uppercase font-semibold font-mono tracking-wider">Hard Bounces</span>
                            <span class="text-lg font-bold text-rose-400">{len(bounces)}</span>
                        </div>
                        <div class="flex items-center justify-between bg-slate-800/50 p-2 rounded-lg border border-slate-700">
                            <span class="text-xs text-slate-300 uppercase font-semibold font-mono tracking-wider">Opt-Outs Scrubbed</span>
                            <span class="text-lg font-bold text-slate-400">{len(optouts)}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Deep Analytics Row (Core 4 Stats) -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="glass p-6 rounded-2xl shadow-lg border-t border-emerald-500/30 flex flex-col justify-center items-center">
                    <h3 class="text-slate-400 font-semibold mb-1 text-center">Total Lifetime Opens</h3>
                    <p class="text-5xl font-black text-white tracking-tight">{open_count}</p>
                </div>
                <div class="glass p-6 rounded-2xl shadow-lg border-t border-purple-500/30 flex flex-col justify-center items-center">
                    <h3 class="text-slate-400 font-semibold mb-1 text-center">Link Clicks</h3>
                    <p class="text-5xl font-black text-purple-400 tracking-tight">{click_count}</p>
                </div>
                <div class="glass p-6 rounded-2xl shadow-lg border-t border-blue-500/30 flex flex-col justify-center items-center">
                    <h3 class="text-slate-400 font-semibold mb-1 text-center">Human Replies</h3>
                    <p class="text-5xl font-black text-white tracking-tight">{len(replies)}</p>
                </div>
                <!-- REVENUE WIDGET -->
                <div class="glass p-6 rounded-2xl shadow-lg border-t border-yellow-400/30 flex flex-col justify-center items-center relative overflow-hidden">
                    <div class="absolute inset-0 bg-yellow-400/5 blur-xl"></div>
                    <h3 class="text-yellow-100 font-semibold mb-1 text-center relative z-10">Sales Revenue</h3>
                    <p class="text-4xl font-black text-yellow-300 tracking-tight relative z-10 cursor-default" title="Pulled straight from pocket_invoices log!">${revenue:,.2f}</p>
                </div>
            </div>

            <div class="flex flex-col gap-8 w-full">
                
                <!-- Top Section (Opens) -->
                <div class="space-y-8 w-full">
                    <!-- Opens Table -->
                    <div class="glass rounded-2xl overflow-hidden shadow-lg">
                        <div class="border-b border-slate-700 bg-slate-800/50 p-4 shrink-0">
                            <h2 class="text-xl font-bold text-emerald-400 flex items-center gap-2">
                                <span>📧</span> Live Email Opens (Recent)
                            </h2>
                        </div>
                        <div class="p-0 overflow-x-auto max-h-[500px] overflow-y-auto">
                            <table class="w-full text-sm text-left">
                                <thead class="text-xs text-slate-400 uppercase bg-slate-800/50 sticky top-0">
                                    <tr>
                                        <th class="px-6 py-3 font-semibold">Time</th>
                                        <th class="px-6 py-3 font-semibold">Email</th>
                                        <th class="px-6 py-3 font-semibold">Campaign</th>
                                    </tr>
                                </thead>
                                <tbody>
"""
    for o in opens:
        dt = o.get("opened_at", "")[:19].replace("T", " ")
        html += f"""
                                    <tr class="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                                        <td class="px-6 py-3 whitespace-nowrap text-slate-300 font-mono text-xs">{dt}</td>
                                        <td class="px-6 py-3 font-medium text-white">{o.get('email', '')}</td>
                                        <td class="px-6 py-3">
                                            <span class="px-2 py-1 text-[10px] font-bold uppercase rounded-full bg-slate-700 text-blue-300 border border-slate-600 tracking-wider">
                                                {o.get('campaign', '')}
                                            </span>
                                        </td>
                                    </tr>
        """
    if not opens:
        html += '<tr><td colspan="3" class="px-6 py-8 text-center text-slate-500">No email opens tracked yet.</td></tr>'
        
    html += """
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Bottom Section (Replies) -->
                <div class="space-y-8 w-full">
                    <!-- Replies Section -->
                    <div class="glass rounded-2xl overflow-hidden shadow-lg max-h-[500px] flex flex-col">
                        <div class="border-b border-slate-700 bg-slate-800/50 p-4 shrink-0 flex justify-between items-center">
                            <h2 class="text-xl font-bold text-blue-400 flex items-center gap-2">
                                <span>💬</span> Human Inbox Replies
                            </h2>
                        </div>
                        <div class="p-4 overflow-y-auto space-y-4">
"""
    if not replies:
        html += '<div class="p-6 text-center text-slate-500">No human replies recorded yet.</div>'
    else:
        for r in replies[:15]:
            html += f"""
                            <div class="bg-slate-800/60 rounded-xl p-4 border border-slate-700 hover:border-blue-500/50 transition-colors">
                                <div class="flex justify-between items-start mb-2">
                                    <div class="font-bold text-white truncate mr-2" title="{r.get('sender', '')}">{r.get('sender', '')}</div>
                                    <div class="text-[10px] text-slate-400 font-mono whitespace-nowrap bg-slate-900/50 px-2 py-1 rounded border border-slate-700">{r.get('date', '')[:22]}</div>
                                </div>
                                <div class="text-sm font-semibold text-blue-300 mb-2 truncate">{r.get('subject', '')}</div>
                                <div class="text-sm text-slate-300 bg-slate-900/50 p-3 rounded-lg leading-relaxed shadow-inner">
                                    "{r.get('snippet', '')}"
                                </div>
                            </div>
            """
    html += """
                        </div>
                    </div>
                </div>

                <!-- Tech Trap Call List Section -->
                <div class="space-y-8 w-full mt-4">
                    <div class="glass rounded-2xl overflow-hidden shadow-lg flex flex-col">
                        <div class="border-b border-slate-700 bg-slate-800/50 p-4 shrink-0 flex justify-between items-center">
                            <h2 class="text-xl font-bold text-fuchsia-400 flex items-center gap-2">
                                <span>📱</span> Tech Trap Call Hit List
                            </h2>
                            <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 bg-fuchsia-500/10 text-fuchsia-300 px-3 py-1.5 rounded-full border border-fuchsia-500/30">Businesses Missing Websites</span>
                        </div>
                        <div class="p-4 overflow-y-auto max-h-[400px]">
                            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
"""
    if call_list_html:
        html += call_list_html
    else:
        html += '<div class="p-6 text-center text-slate-500 col-span-full">No calls generated today.</div>'
        
    html += """
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Email Templates Section -->
                <div class="space-y-8 w-full mt-4">
                    <div class="glass rounded-2xl overflow-hidden shadow-lg">
                        <div class="border-b border-slate-700 bg-slate-800/50 p-4 shrink-0">
                            <h2 class="text-xl font-bold text-orange-400 flex items-center gap-2">
                                <span>✉️</span> Active Drip Sequences In Rotation
                            </h2>
                            <p class="text-[10px] uppercase font-bold tracking-wider text-slate-400 mt-2">Words in <span class="text-amber-300 bg-amber-900/40 px-1 py-0.5 rounded border border-amber-500/30">[brackets]</span> rotate randomly via Spintax logic.</p>
                        </div>
                        <div class="p-6 space-y-8">

                            <!-- Realtor Pitch (NEW) -->
                            <details open class="group bg-slate-900/80 rounded-2xl border border-rose-500/40 shadow-lg relative overflow-hidden transition-all open:bg-slate-900">
                                <summary class="flex justify-between items-center cursor-pointer p-6 list-none z-10 relative select-none outline-none">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2.5 py-1 text-[10px] font-bold tracking-wider uppercase rounded-full bg-rose-500/20 text-rose-300 border border-rose-500/40 shadow">REALTOR CAMPAIGN</span>
                                        <span class="px-2.5 py-1 text-[10px] font-bold tracking-wider uppercase rounded-full bg-slate-800/80 text-white border border-slate-600 shadow">STEP 1 — Creative Hook ($350)</span>
                                    </div>
                                    <span class="transition-transform duration-300 group-open:rotate-180 text-rose-400">
                                        <svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
                                    </span>
                                </summary>
                                <div class="px-6 pb-2 relative z-10">
                                    <p class="text-xs text-slate-400 mb-3 font-mono"><strong>Subject:</strong> {High-end listing graphics 🤔 | Need better content for your properties?}</p>
                                </div>
                                <div class="bg-slate-800/90 p-6 text-[13px] text-slate-200 leading-relaxed border-t border-slate-700 font-sans shadow-inner relative z-10">
                                    <p><span class="text-amber-300 font-medium">[Hey / Hi / Hello]</span> <span class="text-cyan-300 font-medium">[Realtor Name]</span>,</p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[I was browsing local listings and came across your portfolio. / Saw some of your recent listings pop up locally. / I love what you are doing with real estate right now in the area.]</span></p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[I run a creative design agency and we specialize in building ultra-premium social graphics specifically for realtors... / My agency is helping local realtors completely eliminate their content creation headaches...]</span></p>
                                    <br>
                                    <p>We do a <strong class="text-emerald-400">$350 flat-rate package</strong>. You get a massive bundle of fully branded Open House graphics, Just Sold flyers, and Instagram carousels with zero recurring retainer fees.</p>
                                    <br>
                                    <p>Check out our real estate design portfolio here:<br><strong><span class="text-blue-400 hover:text-blue-300 underline cursor-pointer">https://techtrapsolutions.com/realtors</span></strong></p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[Got 5 minutes this week to chat? / Are you open to a quick 5-minute call? / Let me know if you would be open to a quick intro chat.]</span></p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[Best / Cheers / Talk soon]</span>,<br><strong>CeeJay</strong><br><span class="text-rose-300">Tech Trap Solutions</span></p>
                                </div>
                            </details>

                            <!-- Trucking Initial -->
                            <details class="group bg-slate-900/60 rounded-2xl border border-emerald-500/30 shadow-lg relative overflow-hidden transition-all hover:bg-slate-900/80 open:bg-slate-900">
                                <summary class="flex justify-between items-center cursor-pointer p-6 list-none z-10 relative select-none outline-none">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2.5 py-1 text-[10px] font-bold tracking-wider uppercase rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">TRUCKING COMPLIANCE</span>
                                        <span class="px-2.5 py-1 text-[10px] font-bold tracking-wider uppercase rounded-full bg-slate-800 text-slate-300 border border-slate-700">STEP 1 — MC Pitch</span>
                                    </div>
                                    <span class="transition-transform duration-300 group-open:rotate-180 text-emerald-400">
                                        <svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
                                    </span>
                                </summary>
                                <div class="px-6 pb-2 relative z-10">
                                    <p class="text-xs text-slate-400 mb-3 font-mono"><strong>Subject:</strong> {Your new MC Authority | Quick compliance checklist for the new MC | Congrats on the authority}</p>
                                </div>
                                <div class="bg-slate-800/90 p-6 text-[13px] text-slate-300 leading-relaxed border-t border-slate-700 font-sans shadow-inner relative z-10">
                                    <p><span class="text-amber-300 font-medium">[Hey / Hi]</span> <span class="text-cyan-300 font-medium">[Driver Name]</span>,</p>
                                    <br>
                                    <p>Congrats on the new MC Authority! I know the first 90 days are chaotic. Just wanted to shoot over a quick checklist of the critical compliance requirements that most new trucking companies miss (which leads to painful DOT fines).</p>
                                    <br>
                                    <ul class="list-disc pl-5 space-y-2 text-emerald-100/80">
                                        <li><strong>UCR Registration:</strong> Unified Carrier Registration is due before you cross state lines.</li>
                                        <li><strong>BOC-3 Filing:</strong> Process agent designation is legally required for your operating authority.</li>
                                        <li><strong>Drug & Alcohol Consortium:</strong> Mandatory if you operate vehicles over 26k lbs.</li>
                                    </ul>
                                    <br>
                                    <p>My agency handles all this compliance for new authorities so you can focus on finding loads and driving. We do flat-rate setup packages.</p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[Got 5 minutes this week to chat? / Are you open to a quick 5-minute call? / When are you free?]</span></p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[Drive safe / Best / Talk soon]</span>,<br><strong>CeeJay</strong></p>
                                </div>
                            </details>

                            <!-- B2B Initial -->
                            <details class="group bg-slate-900/60 rounded-2xl border border-blue-500/30 shadow-lg relative overflow-hidden transition-all hover:bg-slate-900/80 open:bg-slate-900">
                                <summary class="flex justify-between items-center cursor-pointer p-6 list-none z-10 relative select-none outline-none">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2.5 py-1 text-[10px] font-bold tracking-wider uppercase rounded-full bg-blue-500/20 text-blue-300 border border-blue-500/40">B2B PARTNERSHIP</span>
                                        <span class="px-2.5 py-1 text-[10px] font-bold tracking-wider uppercase rounded-full bg-slate-800 text-slate-300 border border-slate-700">STEP 1 — Revenue Share</span>
                                    </div>
                                    <span class="transition-transform duration-300 group-open:rotate-180 text-blue-400">
                                        <svg fill="none" height="24" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"></path></svg>
                                    </span>
                                </summary>
                                <div class="px-6 pb-2 relative z-10">
                                    <p class="text-xs text-slate-400 mb-3 font-mono"><strong>Subject:</strong> {Partnership opportunity | Connecting in GA | Revenue share for your operations}</p>
                                </div>
                                <div class="bg-slate-800/90 p-6 text-[13px] text-slate-300 leading-relaxed border-t border-slate-700 font-sans shadow-inner relative z-10">
                                    <p><span class="text-amber-300 font-medium">[Hey / Hi / Hello]</span> <span class="text-cyan-300 font-medium">[Name]</span>,</p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[I build custom logistics operations apps and handle compliance for trucking companies... / I run a compliance agency supporting owner-operators...]</span> located right here in GA.</p>
                                    <br>
                                    <p>I'm looking to partner with a few select dispatchers and brokers in the area who already have an established base of owner-operators.</p>
                                    <br>
                                    <p>We pay out a <strong class="text-blue-400">$200 cash commission</strong> for every $1,000 setup package referred to us. It's the highest payout structure in the state because we keep our overhead incredibly low.</p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[I'd love to chat and see if we can build a mutually beneficial pipeline. / Open to a quick intro call this week?]</span></p>
                                    <br>
                                    <p><span class="text-amber-300 font-medium">[Best / Cheers / Talk soon]</span>,<br><strong>CeeJay</strong></p>
                                </div>
                            </details>

                        </div>
                    </div>
                </div>

            </div>
        </div>
        <script>
            document.addEventListener("DOMContentLoaded", () => {
                document.querySelectorAll(".status-dropdown").forEach(select => {
                    let lead = select.getAttribute("data-lead");
                    let savedState = localStorage.getItem("jayboi_status_" + lead);
                    
                    if (savedState) {
                        select.value = savedState;
                        updateColors(select, savedState);
                    }
                    
                    select.addEventListener("change", (e) => {
                        let val = e.target.value;
                        localStorage.setItem("jayboi_status_" + lead, val);
                        updateColors(select, val);
                    });
                });
                
                function updateColors(select, val) {
                    select.classList.remove("bg-slate-900", "bg-emerald-900/50", "bg-rose-900/50", "bg-amber-900/50", "text-emerald-300", "text-rose-300", "text-amber-300", "text-slate-300", "font-bold");
                    
                    if (val === "sold") select.classList.add("bg-emerald-900/50", "text-emerald-300", "font-bold");
                    else if (val === "dead") select.classList.add("bg-rose-900/50", "text-rose-300");
                    else if (val === "contacted") select.classList.add("bg-amber-900/50", "text-amber-300", "font-bold");
                    else select.classList.add("bg-slate-900", "text-slate-300");
                }
                
                // Initialize colors on load
                document.querySelectorAll(".status-dropdown").forEach(select => {
                    updateColors(select, select.value);
                });
            });
        </script>
    </body>
    </html>
    """
    
    with open(HTML_OUTPUT, "w") as f:
        f.write(html)
        
    return HTML_OUTPUT

def main():
    print("[*] Fetching comprehensive analytics data (Opens, Clicks, Revenue)...")
    opens_data = get_opens()
    clicks_data = get_clicks()
    bounces = get_bounces()
    replies = get_replies()
    optouts = get_optouts()
    revenue = get_revenue()
    
    print("[*] Generating local Dashboard HTML v3.0 (Cloud Sync)...")
    html_file = generate_html(opens_data, clicks_data, bounces, replies, optouts, revenue)
    
    print("[+] Omni-Channel Dashboard v3.0 generated successfully!")
    print("[*] Opening dashboard in your web browser...")
    webbrowser.open(f"file://{html_file}")
    
if __name__ == "__main__":
    main()
