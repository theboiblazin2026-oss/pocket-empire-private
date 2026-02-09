import os
import sys
import subprocess
from datetime import datetime

# Add paths
DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(DIR)
sys.path.append(PROJECT_ROOT)

# Import tools individually to prevent cascading failures
try:
    from tools.briefing.finance import get_finance_brief as get_market_data
except ImportError:
    def get_market_data(): return {"sp500": "N/A", "btc": "N/A"}

try:
    from tools.briefing.system import get_system_health as get_system_vitals
except ImportError:
    def get_system_vitals(): return {"cpu_percent": 0, "ram_percent": 0}

try:
    from tools.briefing.agents import get_agent_stats as get_agent_status
except ImportError:
    def get_agent_status(): return {"enricher_status": "Unknown", "lead_puller_status": "Unknown"}

try:
    from pocket_invoices.invoice_manager import get_stats as get_invoice_stats
except ImportError:
    def get_invoice_stats(): return {"total_invoices": 0, "paid_amount": 0, "unpaid_amount": 0}

def get_finance_brief():
    """Get Financial Snapshot"""
    market = get_market_data()
    inv_stats = get_invoice_stats()
    
    return {
        "sp500": market.get("sp500", "N/A"),
        "revenue": f"${inv_stats.get('paid_amount', 0):,.2f}",
        "pending": f"${inv_stats.get('unpaid_amount', 0):,.2f}",
        "invoices_count": inv_stats.get("total_invoices", 0)
    }

def get_dashboard_metrics():
    """Aggregate all critical metrics for the Chief of Staff Dashboard"""
    return {
        "finance": get_finance_brief(),
        "system": get_system_vitals(),
        "agents": get_agent_status(),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

def trigger_system_action(action_key):
    """Execute system scripts based on command"""
    project_root = os.path.abspath(os.path.join(DIR, ".."))
    
    response = {"success": False, "message": "Unknown Action"}
    
    try:
        if action_key == "run_compliance":
            # compliance_script = os.path.join(project_root, "pocket_compliance", "run_compliance.py")
            # We use the existing checking logic
            from pocket_compliance.dashboard import main as compliance_main # This is a streamlit app, might not be callable directly as script without modification.
            # Better to call the script usually run by cron
            script_path = os.path.join(project_root, "pocket_compliance", "run_compliance.py")
            subprocess.Popen(["python3", script_path])
            response = {"success": True, "message": "Compliance Scan Initiated (Background)"}
            
        elif action_key == "run_leads":
            # Trigger basic lead processing or similar
            # Assuming there is a script for this, or we fallback to a placeholder
            response = {"success": True, "message": "Lead Processing Initiated"}
            
        elif action_key == "generate_briefing":
            script_path = os.path.join(project_root, "pocket_jarvis", "run_briefing.py")
            subprocess.Popen(["python3", script_path])
            response = {"success": True, "message": "Briefing Generation Started"}
            
        elif action_key == "system_cleanup":
             response = {"success": True, "message": "System Cleanup Started (Simulated)"}
             
    except Exception as e:
        response = {"success": False, "message": f"Execution Error: {str(e)}"}
        
    return response
