import json
import os
from datetime import datetime, timedelta
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "reminders.json")

def load_reminders():
    """Load reminders from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {"reminders": [], "next_id": 1}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_reminders(data):
    """Save reminders to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def add_reminder(title, due_date, category="personal", recurring=None, 
                 amount=None, payee=None, account=None, notes=None, auto_pay=False):
    """
    Add a new reminder with optional bill details.
    
    Args:
        title: Description of the reminder
        due_date: When it's due (datetime or string)
        category: bills, renewals, inspections, personal
        recurring: None, 'daily', 'weekly', 'monthly', 'yearly'
        amount: Dollar amount (for bills)
        payee: Who to pay (for bills)
        account: Account number/reference (for bills)
        notes: Additional notes
        auto_pay: Whether this is on auto-pay (just tracking)
    
    Returns:
        The created reminder dict
    """
    data = load_reminders()
    
    # Parse date if string
    if isinstance(due_date, str):
        due_date = date_parser.parse(due_date)
    
    reminder = {
        "id": data["next_id"],
        "title": title,
        "due_date": due_date.isoformat(),
        "category": category.lower(),
        "recurring": recurring,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        # Bill-specific fields
        "amount": float(amount) if amount else None,
        "payee": payee,
        "account": account,
        "notes": notes,
        "auto_pay": auto_pay,
        # Tracking
        "payment_history": []
    }
    
    data["reminders"].append(reminder)
    data["next_id"] += 1
    save_reminders(data)
    
    return reminder

def update_reminder(reminder_id, **kwargs):
    """Update a reminder's fields."""
    data = load_reminders()
    
    for r in data["reminders"]:
        if r["id"] == reminder_id:
            for key, value in kwargs.items():
                if key in r:
                    r[key] = value
                elif key == "amount" and value:
                    r["amount"] = float(value)
            save_reminders(data)
            return r
    return None

def get_reminder(reminder_id):
    """Get a single reminder by ID."""
    data = load_reminders()
    for r in data["reminders"]:
        if r["id"] == reminder_id:
            return r
    return None

def get_reminders(include_completed=False, category=None):
    """Get all reminders, optionally filtered."""
    data = load_reminders()
    reminders = data["reminders"]
    
    if not include_completed:
        reminders = [r for r in reminders if not r.get("completed", False)]
    
    if category:
        reminders = [r for r in reminders if r["category"] == category.lower()]
    
    # Sort by due date
    reminders.sort(key=lambda x: x["due_date"])
    
    return reminders

def get_due_reminders(days_ahead=0):
    """Get reminders due within N days (0 = today only)."""
    data = load_reminders()
    today = datetime.now().date()
    cutoff = today + timedelta(days=days_ahead)
    
    due = []
    for r in data["reminders"]:
        if r.get("completed"):
            continue
        due_date = datetime.fromisoformat(r["due_date"]).date()
        if due_date <= cutoff:
            due.append(r)
    
    return sorted(due, key=lambda x: x["due_date"])

def get_monthly_bills_total():
    """Calculate total monthly bills."""
    bills = get_reminders(category="bills")
    total = 0
    for b in bills:
        if b.get("amount"):
            if b.get("recurring") == "yearly":
                total += b["amount"] / 12
            elif b.get("recurring") == "weekly":
                total += b["amount"] * 4
            else:
                total += b["amount"]
    return total

def mark_complete(reminder_id, paid_amount=None):
    """Mark a reminder as complete. If recurring, create next occurrence."""
    data = load_reminders()
    
    for r in data["reminders"]:
        if r["id"] == reminder_id:
            r["completed"] = True
            r["completed_at"] = datetime.now().isoformat()
            
            # Record payment if bill
            if r.get("category") == "bills" and (paid_amount or r.get("amount")):
                if "payment_history" not in r:
                    r["payment_history"] = []
                r["payment_history"].append({
                    "paid_at": datetime.now().isoformat(),
                    "amount": paid_amount or r.get("amount")
                })
            
            # Handle recurring
            if r.get("recurring"):
                old_date = datetime.fromisoformat(r["due_date"])
                
                if r["recurring"] == "daily":
                    new_date = old_date + timedelta(days=1)
                elif r["recurring"] == "weekly":
                    new_date = old_date + timedelta(weeks=1)
                elif r["recurring"] == "monthly":
                    new_date = old_date + relativedelta(months=1)
                elif r["recurring"] == "yearly":
                    new_date = old_date + relativedelta(years=1)
                else:
                    new_date = None
                
                if new_date:
                    # Create next occurrence with same details
                    add_reminder(
                        r["title"],
                        new_date,
                        r["category"],
                        r["recurring"],
                        amount=r.get("amount"),
                        payee=r.get("payee"),
                        account=r.get("account"),
                        notes=r.get("notes"),
                        auto_pay=r.get("auto_pay", False)
                    )
            
            save_reminders(data)
            return True
    
    return False

def delete_reminder(reminder_id):
    """Delete a reminder by ID."""
    data = load_reminders()
    original_len = len(data["reminders"])
    data["reminders"] = [r for r in data["reminders"] if r["id"] != reminder_id]
    
    if len(data["reminders"]) < original_len:
        save_reminders(data)
        return True
    return False

def format_reminder(r):
    """Format a reminder for display."""
    due = datetime.fromisoformat(r["due_date"])
    today = datetime.now().date()
    due_date = due.date()
    
    # Calculate days until due
    days_diff = (due_date - today).days
    
    if days_diff < 0:
        status = f"🔴 OVERDUE by {abs(days_diff)} days"
    elif days_diff == 0:
        status = "🟡 DUE TODAY"
    elif days_diff == 1:
        status = "🟡 Due Tomorrow"
    elif days_diff <= 7:
        status = f"🟢 Due in {days_diff} days"
    else:
        status = f"⚪ Due {due.strftime('%b %d, %Y')}"
    
    cat_emoji = {
        "bills": "💰",
        "renewals": "📋",
        "inspections": "🔧",
        "personal": "📝"
    }.get(r["category"], "📌")
    
    recurring_str = f" (🔄 {r['recurring']})" if r.get("recurring") else ""
    amount_str = f" - ${r['amount']:.2f}" if r.get("amount") else ""
    autopay_str = " [AUTO-PAY]" if r.get("auto_pay") else ""
    
    return f"{cat_emoji} **[{r['id']}]** {r['title']}{amount_str}{recurring_str}{autopay_str}\n   {status}"
