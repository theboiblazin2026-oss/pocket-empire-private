# Lead History & Follow-up Manager
# Tracks contacted leads, conversation history, and follow-up reminders

import json
import os
from datetime import datetime, timedelta

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LEADS_FILE = os.path.join(DATA_DIR, "lead_history.json")

# Lead Status Options
LEAD_STATUSES = [
    "New",
    "Contacted",
    "Interested",
    "Negotiating", 
    "Won",
    "Lost",
    "No Response"
]

def load_leads():
    """Load all tracked leads"""
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_leads(leads):
    """Save leads to file"""
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

def add_lead(company_name, mc_number="", contact_name="", phone="", email="", notes=""):
    """Add a new lead to tracking"""
    leads = load_leads()
    
    lead = {
        "id": datetime.now().timestamp(),
        "company_name": company_name,
        "mc_number": mc_number,
        "contact_name": contact_name,
        "phone": phone,
        "email": email,
        "status": "New",
        "notes": notes,
        "history": [],
        "follow_up_date": None,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    leads.append(lead)
    save_leads(leads)
    return lead

def update_lead_status(lead_id, new_status, notes=""):
    """Update lead status and add to history"""
    leads = load_leads()
    
    for lead in leads:
        if lead["id"] == lead_id:
            old_status = lead["status"]
            lead["status"] = new_status
            lead["updated_at"] = datetime.now().isoformat()
            
            # Add to history
            lead["history"].append({
                "date": datetime.now().isoformat(),
                "action": f"Status: {old_status} → {new_status}",
                "notes": notes
            })
            break
    
    save_leads(leads)

def add_lead_note(lead_id, note, action_type="Note"):
    """Add a note/interaction to lead history"""
    leads = load_leads()
    
    for lead in leads:
        if lead["id"] == lead_id:
            lead["history"].append({
                "date": datetime.now().isoformat(),
                "action": action_type,
                "notes": note
            })
            lead["updated_at"] = datetime.now().isoformat()
            break
    
    save_leads(leads)

def set_follow_up(lead_id, follow_up_date, reminder_note=""):
    """Set a follow-up reminder date"""
    leads = load_leads()
    
    for lead in leads:
        if lead["id"] == lead_id:
            lead["follow_up_date"] = follow_up_date
            lead["history"].append({
                "date": datetime.now().isoformat(),
                "action": "Follow-up Set",
                "notes": f"Reminder: {follow_up_date} - {reminder_note}"
            })
            lead["updated_at"] = datetime.now().isoformat()
            break
    
    save_leads(leads)

def get_due_follow_ups():
    """Get leads with follow-ups due today or overdue"""
    leads = load_leads()
    today = datetime.now().strftime("%Y-%m-%d")
    
    due = []
    for lead in leads:
        if lead.get("follow_up_date"):
            if lead["follow_up_date"] <= today:
                due.append(lead)
    
    return due

def get_upcoming_follow_ups(days=7):
    """Get follow-ups coming up in the next X days"""
    leads = load_leads()
    today = datetime.now()
    cutoff = (today + timedelta(days=days)).strftime("%Y-%m-%d")
    today_str = today.strftime("%Y-%m-%d")
    
    upcoming = []
    for lead in leads:
        if lead.get("follow_up_date"):
            if today_str < lead["follow_up_date"] <= cutoff:
                upcoming.append(lead)
    
    return upcoming

def get_lead_by_id(lead_id):
    """Get a specific lead by ID"""
    leads = load_leads()
    for lead in leads:
        if lead["id"] == lead_id:
            return lead
    return None

def delete_lead(lead_id):
    """Delete a lead from tracking"""
    leads = load_leads()
    leads = [l for l in leads if l["id"] != lead_id]
    save_leads(leads)

def get_leads_by_status(status):
    """Filter leads by status"""
    leads = load_leads()
    return [l for l in leads if l["status"] == status]

def search_leads(query):
    """Search leads by company name, contact, or MC number"""
    leads = load_leads()
    query = query.lower()
    
    results = []
    for lead in leads:
        if (query in lead.get("company_name", "").lower() or
            query in lead.get("contact_name", "").lower() or
            query in lead.get("mc_number", "").lower()):
            results.append(lead)
    
    return results

def get_lead_stats():
    """Get pipeline statistics"""
    leads = load_leads()
    
    stats = {status: 0 for status in LEAD_STATUSES}
    for lead in leads:
        status = lead.get("status", "New")
        if status in stats:
            stats[status] += 1
    
    stats["total"] = len(leads)
    stats["due_today"] = len(get_due_follow_ups())
    
    return stats
