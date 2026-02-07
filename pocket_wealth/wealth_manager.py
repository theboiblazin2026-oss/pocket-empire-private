import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Default Template
DEFAULT_BUDGET = {
    "daily_target": 152.00,
    "monthly_bills": [
        {"name": "Rent", "amount": 800.00, "category": "housing"},
        {"name": "Car Payment", "amount": 400.00, "category": "transport"},
        {"name": "Car Insurance", "amount": 200.00, "category": "transport"},
        {"name": "Phone Bill", "amount": 100.00, "category": "utilities"},
        {"name": "Groceries", "amount": 400.00, "category": "food"},
        {"name": "Gas", "amount": 400.00, "category": "transport"},
        {"name": "Misc/Buffer", "amount": 235.00, "category": "other"}
    ],
    "income_streams": [
        {"name": "Gig Work (Uber/DoorDash)", "type": "variable"},
        {"name": "Trucking Business", "type": "variable"}
    ]
}

def get_client_file(client_name):
    # Sanitize name for filename
    safe_name = "".join([c for c in client_name if c.isalpha() or c.isdigit() or c==' ']).strip().replace(' ', '_')
    return os.path.join(DATA_DIR, f"{safe_name}_wealth.json")

def load_data(client_name):
    filepath = get_client_file(client_name)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {
        "budget": DEFAULT_BUDGET,
        "daily_log": [],
        "net_worth_history": []
    }

def save_data(client_name, data):
    filepath = get_client_file(client_name)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def update_budget(client_name, daily_target, bills, streams):
    data = load_data(client_name)
    data["budget"] = {
        "daily_target": float(daily_target),
        "monthly_bills": bills,
        "income_streams": streams
    }
    save_data(client_name, data)

def log_earnings(client_name, amount, source="Gig Work", notes=""):
    data = load_data(client_name)
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "amount": float(amount),
        "source": source,
        "notes": notes
    }
    data["daily_log"].append(entry)
    save_data(client_name, data)
    return entry

def get_daily_progress(client_name):
    data = load_data(client_name)
    today = datetime.now().strftime("%Y-%m-%d")
    
    earned_today = sum(e["amount"] for e in data["daily_log"] if e.get("date") == today)
    target = data["budget"]["daily_target"]
    remaining = target - earned_today
    
    return {
        "earned": earned_today,
        "target": target,
        "remaining": max(0, remaining),
        "percent": min(100, int((earned_today / target) * 100)) if target > 0 else 100
    }
