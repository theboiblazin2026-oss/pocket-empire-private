import json
import os
from datetime import datetime
import pandas as pd

# Load Management for Personal Dispatch
# Tracks loads, rates, and status (Booked -> Rolling -> Delivered -> Paid)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pocket_leads", "data")
LOADS_FILE = os.path.join(DATA_DIR, "dispatch_loads.json")

# Ensure data dir exists (reuses pocket_leads data dir for simplicity)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOAD_STATUSES = [
    "Booked",
    "Dispatched", 
    "At Pickup",
    "In Transit",
    "At Delivery",
    "Delivered",
    "Invoiced",
    "Paid",
    "Cancelled"
]

def load_all_loads():
    """Load all tracked loads"""
    if os.path.exists(LOADS_FILE):
        with open(LOADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_loads(loads):
    """Save loads to file"""
    with open(LOADS_FILE, 'w') as f:
        json.dump(loads, f, indent=2)

def create_load(broker_name, origin, destination, rate, pickup_date, delivery_date, weight=0, commodity=""):
    """Create a new load"""
    loads = load_all_loads()
    
    new_load = {
        "id": f"LOAD-{int(datetime.now().timestamp())}",
        "broker": broker_name,
        "origin": origin,
        "destination": destination,
        "rate": float(rate),
        "pickup_date": str(pickup_date),
        "delivery_date": str(delivery_date),
        "weight": weight,
        "commodity": commodity,
        "status": "Booked",
        "notes": "",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "history": [{
            "date": datetime.now().isoformat(),
            "action": "Load Created",
            "details": f"Rate: ${rate} | Lane: {origin} -> {destination}"
        }]
    }
    
    loads.append(new_load)
    save_loads(loads)
    return new_load

def update_load_status(load_id, new_status, note=""):
    """Update load status"""
    loads = load_all_loads()
    for load in loads:
        if load["id"] == load_id:
            old = load["status"]
            load["status"] = new_status
            load["updated_at"] = datetime.now().isoformat()
            
            load["history"].append({
                "date": datetime.now().isoformat(),
                "action": f"Status Change: {old} -> {new_status}",
                "details": note
            })
            save_loads(loads)
            return True
    return False

def get_weekly_revenue():
    """Calculate revenue for current week"""
    loads = load_all_loads()
    today = datetime.now()
    # Simple calculation of all loads created/active in last 7 days for now
    # Or just sum by status
    
    revenue = {
        "booked": 0.0,
        "rolling": 0.0,
        "delivered": 0.0,
        "paid": 0.0,
        "total": 0.0
    }
    
    for load in loads:
        rate = load.get("rate", 0.0)
        status = load.get("status", "Booked")
        
        if status == "Cancelled":
            continue
            
        revenue["total"] += rate
        
        if status in ["Booked", "Dispatched"]:
            revenue["booked"] += rate
        elif status in ["At Pickup", "In Transit", "At Delivery"]:
            revenue["rolling"] += rate
        elif status in ["Delivered", "Invoiced"]:
            revenue["delivered"] += rate
        elif status == "Paid":
            revenue["paid"] += rate
            
    return revenue

def delete_load(load_id):
    """Delete a load"""
    loads = load_all_loads()
    loads = [l for l in loads if l["id"] != load_id]
    save_loads(loads)
