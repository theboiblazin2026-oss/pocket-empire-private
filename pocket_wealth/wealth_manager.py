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
    # Try DB First
    try:
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
        import db
        client = db.get_db()
        if client:
            key = f"wealth_{client_name}"
            res = client.table("app_data").select("value").eq("key", key).execute()
            if res.data:
                return res.data[0]['value']
    except:
        pass

    # Fallback to Local
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
    # Local Save
    filepath = get_client_file(client_name)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
        
    # DB Save
    try:
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
        import db
        client = db.get_db()
        if client:
            key = f"wealth_{client_name}"
            payload = {
                "key": key,
                "value": data,
                "updated_at": datetime.now().isoformat()
            }
            client.table("app_data").upsert(payload).execute()
    except Exception as e:
        print(f"Wealth Sync Error: {e}")

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

# ============== NET WORTH TRACKER ==============

def save_net_worth_snapshot(client_name, assets, debts):
    """Save a snapshot of net worth with detailed breakdown"""
    data = load_data(client_name)
    
    total_assets = sum(assets.values())
    total_debts = sum(debts.values())
    net_worth = total_assets - total_debts
    
    snapshot = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat(),
        "assets": assets,
        "debts": debts,
        "total_assets": total_assets,
        "total_debts": total_debts,
        "net_worth": net_worth
    }
    
    if "net_worth_history" not in data:
        data["net_worth_history"] = []
    
    # Replace today's snapshot if exists, otherwise append
    today = datetime.now().strftime("%Y-%m-%d")
    data["net_worth_history"] = [s for s in data["net_worth_history"] if s.get("date") != today]
    data["net_worth_history"].append(snapshot)
    
    save_data(client_name, data)
    return snapshot

def get_net_worth_history(client_name, limit=30):
    """Get net worth snapshots for charting"""
    data = load_data(client_name)
    history = data.get("net_worth_history", [])
    return sorted(history, key=lambda x: x.get("date", ""), reverse=True)[:limit]

def get_latest_net_worth(client_name):
    """Get the most recent net worth snapshot"""
    history = get_net_worth_history(client_name, limit=1)
    if history:
        return history[0]
    return {"net_worth": 0, "total_assets": 0, "total_debts": 0, "assets": {}, "debts": {}}

# ============== DEBT TRACKER ==============

def get_debts(client_name):
    """Get all tracked debts"""
    data = load_data(client_name)
    return data.get("debts", [])

def add_debt(client_name, name, original_balance, current_balance, min_payment=0, interest_rate=0):
    """Add a new debt to track"""
    data = load_data(client_name)
    
    if "debts" not in data:
        data["debts"] = []
    
    debt = {
        "id": datetime.now().timestamp(),
        "name": name,
        "original_balance": float(original_balance),
        "current_balance": float(current_balance),
        "min_payment": float(min_payment),
        "interest_rate": float(interest_rate),
        "payments": [],
        "created_at": datetime.now().isoformat()
    }
    
    data["debts"].append(debt)
    save_data(client_name, data)
    return debt

def log_debt_payment(client_name, debt_id, amount, notes=""):
    """Log a payment against a debt"""
    data = load_data(client_name)
    
    for debt in data.get("debts", []):
        if debt["id"] == debt_id:
            debt["current_balance"] = max(0, debt["current_balance"] - amount)
            debt["payments"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "amount": float(amount),
                "notes": notes,
                "new_balance": debt["current_balance"]
            })
            break
    
    save_data(client_name, data)

def delete_debt(client_name, debt_id):
    """Remove a debt from tracking"""
    data = load_data(client_name)
    data["debts"] = [d for d in data.get("debts", []) if d["id"] != debt_id]
    save_data(client_name, data)

# ============== SAVINGS GOALS ==============

def get_savings_goals(client_name):
    """Get all savings goals"""
    data = load_data(client_name)
    return data.get("savings_goals", [])

def add_savings_goal(client_name, name, target_amount, current_amount=0, deadline=None):
    """Add a new savings goal"""
    data = load_data(client_name)
    
    if "savings_goals" not in data:
        data["savings_goals"] = []
    
    goal = {
        "id": datetime.now().timestamp(),
        "name": name,
        "target_amount": float(target_amount),
        "current_amount": float(current_amount),
        "deadline": deadline,
        "contributions": [],
        "created_at": datetime.now().isoformat()
    }
    
    data["savings_goals"].append(goal)
    save_data(client_name, data)
    return goal

def contribute_to_goal(client_name, goal_id, amount, notes=""):
    """Add money to a savings goal"""
    data = load_data(client_name)
    
    for goal in data.get("savings_goals", []):
        if goal["id"] == goal_id:
            goal["current_amount"] += float(amount)
            goal["contributions"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "amount": float(amount),
                "notes": notes
            })
            break
    
    save_data(client_name, data)

def delete_savings_goal(client_name, goal_id):
    """Remove a savings goal"""
    data = load_data(client_name)
    data["savings_goals"] = [g for g in data.get("savings_goals", []) if g["id"] != goal_id]
    save_data(client_name, data)

def get_total_debt(client_name):
    """Get total current debt balance"""
    debts = get_debts(client_name)
    return sum(d.get("current_balance", 0) for d in debts)

def get_total_savings(client_name):
    """Get total saved towards all goals"""
    goals = get_savings_goals(client_name)
    return sum(g.get("current_amount", 0) for g in goals)

