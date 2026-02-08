import os
import json
import glob
import pandas as pd

def search_app(query):
    """
    Searches across Leads, Wealth Profiles, and Saved Routes for the query string.
    Returns a list of dictionaries with keys: Type, Name, Details, Page.
    """
    results = []
    query = query.lower()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # --- 1. Search Leads ---
    try:
        leads_path = os.path.join(base_dir, 'pocket_leads', 'leads.json')
        if os.path.exists(leads_path):
            with open(leads_path, 'r') as f:
                leads = json.load(f)
                for lead in leads:
                    # Search text: Company, Contact, Status, Notes
                    searchable_text = f"{lead.get('Company', '')} {lead.get('Contact', '')} {lead.get('Status', '')} {lead.get('Notes', '')}".lower()
                    
                    if query in searchable_text:
                        results.append({
                            "Type": "Lead",
                            "Name": lead.get('Company', 'Unknown'),
                            "Details": f"Status: {lead.get('Status')} | Contact: {lead.get('Contact')}",
                            "Page": "pages/06_📋_Lead_Pipeline.py"
                        })
    except Exception as e:
        print(f"Search Error (Leads): {e}")

    # --- 2. Search Wealth (Budgets/Debts) ---
    try:
        wealth_dir = os.path.join(base_dir, 'pocket_wealth')
        # Check specific client files (naming convention wealth_*.json) or just scan directory
        # Based on previous exploration, let's look for json files in pocket_wealth/data if it exists
        # or simplified: check known profiles if possible, but scanning generic json is safer for broad search
        
        # Let's try scanning for client_*.json or just general JSONs in a 'data' folder if used
        # Reverting to safer "client_manager" check if possible, but for now simple file scan
        # defined in wealth_manager.py: get_client_file uses 'data' dir probably?
        # Let's assume pocket_wealth/*.json or pocket_wealth/data/*.json
        
        search_paths = [
            os.path.join(wealth_dir, "*.json"),
            os.path.join(wealth_dir, "data", "*.json")
        ]
        
        for pattern in search_paths:
            for filepath in glob.glob(pattern):
                filename = os.path.basename(filepath)
                if filename.startswith("wealth_") or filename == "myself.json" or "budget" in filename:
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            
                        # Search Budget Items
                        found_match = False
                        match_details = ""
                        
                        # Check Bills
                        for bill in data.get("budget", {}).get("monthly_bills", []):
                            if query in bill.get("name", "").lower():
                                found_match = True
                                match_details = f"Bill: {bill['name']}"
                                break
                                
                        # Check Income
                        if not found_match:
                            for stream in data.get("budget", {}).get("income_streams", []):
                                if query in stream.get("name", "").lower():
                                    found_match = True
                                    match_details = f"Income: {stream['name']}"
                                    break
                                    
                        # Check Debts
                        if not found_match:
                            for debt in data.get("debts", []): # Structure varies, check if key exists
                                if query in debt.get("name", "").lower():
                                    found_match = True
                                    match_details = f"Debt: {debt['name']}"
                                    break

                        if found_match:
                             client_name = filename.replace("wealth_", "").replace(".json", "")
                             results.append({
                                "Type": "Budget",
                                "Name": client_name.capitalize(),
                                "Details": match_details,
                                "Page": "pages/01_💰_Wealth_Manager.py"
                            })
                    except:
                        continue
    except Exception as e:
        print(f"Search Error (Wealth): {e}")

    # --- 3. Search Routes ---
    try:
        routes_dir = os.path.join(base_dir, 'pocket_router', 'saved_routes')
        if os.path.exists(routes_dir):
            for filepath in glob.glob(os.path.join(routes_dir, "*.json")):
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    
                    # Search Route Name and Stops
                    route_name = data.get("name", os.path.basename(filepath)).lower()
                    stops = " ".join([wp.get("name", "") for wp in data.get("waypoints", [])]).lower()
                    
                    if query in route_name or query in stops:
                        results.append({
                            "Type": "Route",
                            "Name": data.get("name", "Unnamed Route"),
                            "Details": f"{len(data.get('waypoints', []))} stops",
                            "Page": "pages/10_🛣️_Route_Planner.py"
                        })
                except:
                    continue
    except Exception as e:
        print(f"Search Error (Routes): {e}")

    return results
