"""
Rate Negotiator - Track lane rates, broker profiles, and generate negotiation scripts
"""
import json
import os
from datetime import datetime, timedelta
from statistics import mean, median

DATA_FILE = os.path.join(os.path.dirname(__file__), "rates.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"lanes": [], "brokers": [], "rate_history": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def normalize_city(city):
    """Normalize city names for matching"""
    return city.strip().upper().replace(",", "").replace(".", "")


def get_lane_key(origin, destination):
    """Create a consistent lane key"""
    return f"{normalize_city(origin)}|{normalize_city(destination)}"


def add_rate_entry(origin, destination, rate, miles, broker_name=None, accepted=False, notes=None):
    """Add a rate quote/acceptance to history"""
    data = load_data()
    
    entry = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S"),
        "origin": origin.strip(),
        "destination": destination.strip(),
        "lane_key": get_lane_key(origin, destination),
        "rate": float(rate),
        "miles": int(miles) if miles else None,
        "rate_per_mile": round(float(rate) / int(miles), 2) if miles and int(miles) > 0 else None,
        "broker": broker_name.strip() if broker_name else None,
        "accepted": accepted,
        "notes": notes,
        "date": datetime.now().isoformat()
    }
    
    data["rate_history"].append(entry)
    
    # Update lane stats
    lane_key = entry["lane_key"]
    lane = next((l for l in data["lanes"] if l["key"] == lane_key), None)
    
    if not lane:
        lane = {
            "key": lane_key,
            "origin": origin.strip(),
            "destination": destination.strip(),
            "quotes": 0,
            "accepted": 0,
            "total_rate": 0,
            "avg_rate": 0,
            "avg_rpm": 0,
            "last_quoted": None
        }
        data["lanes"].append(lane)
    
    lane["quotes"] += 1
    if accepted:
        lane["accepted"] += 1
    lane["total_rate"] += entry["rate"]
    lane["avg_rate"] = round(lane["total_rate"] / lane["quotes"], 2)
    if entry["rate_per_mile"]:
        # Approximate - could be more precise with stored values
        lane["avg_rpm"] = entry["rate_per_mile"]
    lane["last_quoted"] = entry["date"]
    
    # Update broker if provided
    if broker_name:
        broker = next((b for b in data["brokers"] if b["name"].upper() == broker_name.upper()), None)
        if not broker:
            broker = {
                "name": broker_name.strip(),
                "quotes": 0,
                "accepted": 0,
                "avg_rate_diff": 0,
                "notes": []
            }
            data["brokers"].append(broker)
        broker["quotes"] += 1
        if accepted:
            broker["accepted"] += 1
    
    save_data(data)
    return entry


def get_lane_stats(origin, destination):
    """Get statistics for a specific lane"""
    data = load_data()
    lane_key = get_lane_key(origin, destination)
    
    # Get all entries for this lane
    entries = [e for e in data["rate_history"] if e["lane_key"] == lane_key]
    
    if not entries:
        return None
    
    rates = [e["rate"] for e in entries]
    rpms = [e["rate_per_mile"] for e in entries if e["rate_per_mile"]]
    accepted = [e for e in entries if e["accepted"]]
    
    # Recent entries (last 30 days)
    cutoff = datetime.now() - timedelta(days=30)
    recent = [e for e in entries if datetime.fromisoformat(e["date"]) > cutoff]
    
    stats = {
        "lane": f"{entries[0]['origin']} → {entries[0]['destination']}",
        "total_quotes": len(entries),
        "accepted_count": len(accepted),
        "acceptance_rate": round(len(accepted) / len(entries) * 100, 1) if entries else 0,
        "avg_rate": round(mean(rates), 2),
        "min_rate": min(rates),
        "max_rate": max(rates),
        "avg_rpm": round(mean(rpms), 2) if rpms else None,
        "recent_count": len(recent),
        "recent_avg": round(mean([e["rate"] for e in recent]), 2) if recent else None,
        "trend": None
    }
    
    # Calculate trend (is recent avg higher or lower than overall?)
    if stats["recent_avg"] and len(recent) >= 2:
        diff = stats["recent_avg"] - stats["avg_rate"]
        if diff > 50:
            stats["trend"] = "📈 UP"
        elif diff < -50:
            stats["trend"] = "📉 DOWN"
        else:
            stats["trend"] = "➡️ STABLE"
    
    return stats


def get_broker_profile(broker_name):
    """Get profile for a specific broker"""
    data = load_data()
    broker = next((b for b in data["brokers"] if b["name"].upper() == broker_name.upper()), None)
    
    if not broker:
        return None
    
    # Get their rate history
    entries = [e for e in data["rate_history"] if e.get("broker", "").upper() == broker_name.upper()]
    
    profile = {
        "name": broker["name"],
        "total_quotes": broker["quotes"],
        "accepted_quotes": broker["accepted"],
        "acceptance_rate": round(broker["accepted"] / broker["quotes"] * 100, 1) if broker["quotes"] else 0,
        "lanes_quoted": list(set(e["lane_key"].replace("|", " → ") for e in entries)),
        "avg_rate": round(mean([e["rate"] for e in entries]), 2) if entries else 0,
        "notes": broker.get("notes", [])
    }
    
    # Rate quality assessment
    if profile["acceptance_rate"] >= 50:
        profile["rating"] = "✅ GOOD - Often pays fair rates"
    elif profile["acceptance_rate"] >= 25:
        profile["rating"] = "🟡 OKAY - Sometimes competitive"
    else:
        profile["rating"] = "🔴 LOWBALLER - Rarely accepts good rates"
    
    return profile


def generate_negotiation_script(origin, destination, offered_rate, miles=None):
    """Generate a negotiation script based on lane history"""
    data = load_data()
    stats = get_lane_stats(origin, destination)
    
    offered = float(offered_rate)
    
    scripts = []
    
    if stats:
        avg_rate = stats["avg_rate"]
        diff = offered - avg_rate
        diff_percent = round((diff / avg_rate) * 100, 1)
        
        # Calculate counter offer (15% premium over their offer, or at least avg)
        counter = max(offered * 1.15, avg_rate)
        counter = round(counter, -1)  # Round to nearest 10
        
        if diff_percent < -20:
            # Way below market
            scripts.append({
                "type": "🔴 LOWBALL ALERT",
                "message": f"Their offer of ${offered:,.0f} is {abs(diff_percent)}% BELOW your average of ${avg_rate:,.0f} for this lane.",
                "script": f"Thanks for reaching out, but this lane typically pays around ${avg_rate:,.0f}. Your offer of ${offered:,.0f} is significantly below market. I'd need at least ${counter:,.0f} to make this work."
            })
        elif diff_percent < -10:
            # Below market
            scripts.append({
                "type": "🟠 BELOW MARKET",
                "message": f"Offer is {abs(diff_percent)}% below your average of ${avg_rate:,.0f}.",
                "script": f"I appreciate the offer. Based on what this lane usually pays, I'm looking for closer to ${counter:,.0f}. Can you work with that?"
            })
        elif diff_percent < 5:
            # Around market
            scripts.append({
                "type": "🟡 FAIR OFFER",
                "message": f"Offer is close to your average of ${avg_rate:,.0f}.",
                "script": f"That's in the ballpark. I can do ${counter:,.0f} and we have a deal."
            })
        else:
            # Above market
            scripts.append({
                "type": "✅ GOOD OFFER",
                "message": f"Offer is {diff_percent}% ABOVE your average of ${avg_rate:,.0f}!",
                "script": f"That works for me. I can confirm at ${offered:,.0f}. When's pickup?"
            })
    else:
        # No history for this lane
        if miles:
            # Estimate based on per-mile rate
            target_rpm = 2.50  # Default target rate per mile
            estimated_rate = int(miles) * target_rpm
            counter = round(max(offered * 1.15, estimated_rate), -1)
            
            scripts.append({
                "type": "📊 NEW LANE - NO HISTORY",
                "message": f"No rate history for this lane. Using ${target_rpm:.2f}/mile as baseline (${estimated_rate:,.0f} for {miles} miles).",
                "script": f"I don't have recent data on this lane, but based on {miles} miles at current market rates, I'm looking for ${counter:,.0f}. Can you work with that?"
            })
        else:
            scripts.append({
                "type": "📊 NEW LANE - NO HISTORY",
                "message": "No rate history or mileage provided. Consider researching comparable lanes.",
                "script": f"What's the mileage on this? Let me check what similar lanes are paying before I commit."
            })
    
    return scripts


def get_all_lanes():
    """Get all tracked lanes"""
    data = load_data()
    return sorted(data.get("lanes", []), key=lambda x: x.get("quotes", 0), reverse=True)


def get_all_brokers():
    """Get all tracked brokers"""
    data = load_data()
    return sorted(data.get("brokers", []), key=lambda x: x.get("quotes", 0), reverse=True)


def get_recent_rates(limit=20):
    """Get recent rate entries"""
    data = load_data()
    return data.get("rate_history", [])[-limit:]


if __name__ == "__main__":
    # Test
    print("Rate Negotiator initialized")
    print(f"Data file: {DATA_FILE}")
