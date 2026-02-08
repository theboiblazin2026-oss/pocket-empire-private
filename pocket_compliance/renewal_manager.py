# Compliance Renewal Alert Manager
# Tracks expiration dates for trucking compliance items and generates alerts

import json
import os
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "renewals.json")

# Standard trucking compliance items with typical renewal periods
RENEWAL_TYPES = [
    {"name": "MC Authority", "months": 0, "description": "Continuous - but check for revocation"},
    {"name": "USDOT Biennial Update", "months": 24, "description": "Every 2 years"},
    {"name": "UCR Registration", "months": 12, "description": "Unified Carrier - Annual"},
    {"name": "IFTA License", "months": 12, "description": "International Fuel Tax - Annual"}, 
    {"name": "IRP Registration", "months": 12, "description": "International Registration Plan - Annual"},
    {"name": "BOC-3 (Process Agent)", "months": 0, "description": "Continuous unless changed"},
    {"name": "Insurance (Liability)", "months": 12, "description": "Annual policy renewal"},
    {"name": "Insurance (Cargo)", "months": 12, "description": "Annual policy renewal"},
    {"name": "Drug & Alcohol Consortium", "months": 12, "description": "Annual membership"},
    {"name": "Driver Qualification Files", "months": 12, "description": "Annual MVR review"},
    {"name": "Vehicle Registration", "months": 12, "description": "State registration - Annual"},
    {"name": "Annual Vehicle Inspection", "months": 12, "description": "FMCSA required"},
    {"name": "Fire Extinguisher Inspection", "months": 12, "description": "Annual"},
    {"name": "Hazmat Endorsement", "months": 60, "description": "Every 5 years"},
]

def load_renewals():
    """Load all tracked renewals"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"items": [], "last_updated": None}

def save_renewals(data):
    """Save renewals data"""
    data["last_updated"] = datetime.now().isoformat()
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_renewal_item(name, expiration_date, notes="", reminder_days=30):
    """Add a new renewal item to track"""
    data = load_renewals()
    
    item = {
        "id": datetime.now().timestamp(),
        "name": name,
        "expiration_date": expiration_date,
        "notes": notes,
        "reminder_days": reminder_days,
        "created_at": datetime.now().isoformat(),
        "completed": False
    }
    
    data["items"].append(item)
    save_renewals(data)
    return item

def update_renewal(item_id, expiration_date=None, notes=None, completed=None):
    """Update a renewal item"""
    data = load_renewals()
    
    for item in data["items"]:
        if item["id"] == item_id:
            if expiration_date:
                item["expiration_date"] = expiration_date
            if notes is not None:
                item["notes"] = notes
            if completed is not None:
                item["completed"] = completed
            item["updated_at"] = datetime.now().isoformat()
            break
    
    save_renewals(data)

def delete_renewal(item_id):
    """Delete a renewal item"""
    data = load_renewals()
    data["items"] = [i for i in data["items"] if i["id"] != item_id]
    save_renewals(data)

def get_all_renewals():
    """Get all renewal items sorted by expiration date"""
    data = load_renewals()
    items = [i for i in data["items"] if not i.get("completed", False)]
    return sorted(items, key=lambda x: x.get("expiration_date", "9999-12-31"))

def get_expired_items():
    """Get items that have already expired"""
    today = datetime.now().strftime("%Y-%m-%d")
    items = get_all_renewals()
    return [i for i in items if i.get("expiration_date", "9999-12-31") < today]

def get_due_soon(days=30):
    """Get items expiring within X days"""
    today = datetime.now()
    cutoff = (today + timedelta(days=days)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")
    
    items = get_all_renewals()
    return [i for i in items if today_str <= i.get("expiration_date", "9999-12-31") <= cutoff]

def get_upcoming(days_from=31, days_to=90):
    """Get items expiring between X and Y days"""
    today = datetime.now()
    start = (today + timedelta(days=days_from)).strftime("%Y-%m-%d")
    end = (today + timedelta(days=days_to)).strftime("%Y-%m-%d")
    
    items = get_all_renewals()
    return [i for i in items if start <= i.get("expiration_date", "9999-12-31") <= end]

def get_alert_summary():
    """Get a summary of alerts for dashboard display"""
    expired = get_expired_items()
    due_soon = get_due_soon(30)
    upcoming = get_upcoming(31, 90)
    
    return {
        "expired_count": len(expired),
        "due_soon_count": len(due_soon),
        "upcoming_count": len(upcoming),
        "expired": expired,
        "due_soon": due_soon,
        "upcoming": upcoming,
        "status": "🔴 CRITICAL" if expired else ("🟡 WARNING" if due_soon else "🟢 OK")
    }

def mark_renewed(item_id, new_expiration_date):
    """Mark an item as renewed with new expiration date"""
    data = load_renewals()
    
    for item in data["items"]:
        if item["id"] == item_id:
            # Save old date in history
            if "history" not in item:
                item["history"] = []
            item["history"].append({
                "old_date": item["expiration_date"],
                "renewed_on": datetime.now().isoformat()
            })
            
            item["expiration_date"] = new_expiration_date
            item["updated_at"] = datetime.now().isoformat()
            break
    
    save_renewals(data)
