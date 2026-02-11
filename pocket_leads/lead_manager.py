"""
Lead Qualifier - Score carriers/companies based on authority, safety, and risk factors
"""
import json
import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

DATA_FILE = os.path.join(os.path.dirname(__file__), "leads.json")

def load_data():
    # Try DB First
    try:
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
        import db
        client = db.get_db()
        if client:
            key = "leads_history"
            res = client.table("app_data").select("value").eq("key", key).execute()
            if res.data:
                return res.data[0]['value']
    except:
        pass

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"scored_leads": [], "score_history": []}

def save_data(data):
    # Local Save
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        
    # DB Save
    try:
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../pocket_core')))
        import db
        client = db.get_db()
        if client:
            key = "leads_history"
            payload = {
                "key": key,
                "value": data,
                "updated_at": datetime.now().isoformat()
            }
            client.table("app_data").upsert(payload).execute()
    except Exception as e:
        print(f"Lead Sync Error: {e}")

def get_carrier_info(identifier, search_type="MC_MX"):
    """Fetch carrier info from FMCSA SAFER"""
    s = requests.Session()
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0'
    })
    
    try:
        url = "https://safer.fmcsa.dot.gov/query.asp"
        payload = {
            "searchtype": "ANY",
            "query_type": "queryCarrierSnapshot",
            "query_param": search_type,
            "query_string": identifier.strip()
        }
        r = s.post(url, data=payload, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        if "Company Snapshot" not in r.text or "Record Not Found" in r.text:
            return {"error": "Not Found / Invalid ID"}
        
        data = {
            "legal_name": "Unknown",
            "dba_name": None,
            "dot_number": None,
            "mc_number": None,
            "status": "Unknown",
            "safety_rating": "None",
            "authority_granted": None,
            "power_units": 0,
            "drivers": 0,
            "mcs150_date": None,
            "insurance_status": "Unknown"
        }
        
        # Extract Legal Name
        for label in ["Legal Name:", "Name:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                td = anchor.find_parent("th")
                if td:
                    td = td.find_next_sibling("td")
                    if td:
                        data['legal_name'] = td.text.strip()
                        break
        
        # Extract DBA Name
        anchor = soup.find("a", string="DBA Name:")
        if anchor:
            td = anchor.find_parent("th")
            if td:
                td = td.find_next_sibling("td")
                if td:
                    data['dba_name'] = td.text.strip()
        
        # Extract USDOT Number
        anchor = soup.find("a", string="USDOT Number:")
        if anchor:
            td = anchor.find_parent("th")
            if td:
                td = td.find_next_sibling("td")
                if td:
                    data['dot_number'] = td.text.strip()
        
        # Extract MC/MX Number
        for label in ["MC/MX/FF Number(s):", "MC Number:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                td = anchor.find_parent("th")
                if td:
                    td = td.find_next_sibling("td")
                    if td:
                        mc_text = td.text.strip()
                        # Extract just the MC number
                        if "MC-" in mc_text:
                            data['mc_number'] = mc_text.split("MC-")[1].split()[0].strip()
                        break
        
        # Extract Operating Status
        for label in ["USDOT Status:", "Operating Status:", "Status:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                td = anchor.find_parent("th")
                if td:
                    td = td.find_next_sibling("td")
                    if td:
                        val = td.text.strip().upper()
                        if "ACTIVE" in val:
                            data['status'] = "ACTIVE"
                        elif "INACTIVE" in val:
                            data['status'] = "INACTIVE"
                        elif "OUT-OF-SERVICE" in val or "OUT OF SERVICE" in val:
                            data['status'] = "OUT-OF-SERVICE"
                        break
        
        # Extract Safety Rating
        for label in ["Safety Rating:", "Rating:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                td = anchor.find_parent("th")
                if td:
                    td = td.find_next_sibling("td")
                    if td:
                        val = td.text.strip()
                        if "Satisfactory" in val:
                            data['safety_rating'] = "Satisfactory"
                        elif "Conditional" in val:
                            data['safety_rating'] = "Conditional"
                        elif "Unsatisfactory" in val:
                            data['safety_rating'] = "Unsatisfactory"
                        else:
                            data['safety_rating'] = "None"
                        break
        
        # Extract MCS-150 Date (used to calculate authority age)
        anchor = soup.find("a", string="MCS-150 Form Date:")
        if anchor:
            td = anchor.find_parent("th")
            if td:
                td = td.find_next_sibling("td")
                if td:
                    date_text = td.text.strip()
                    try:
                        # Try to parse date (format varies)
                        for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y"]:
                            try:
                                data['mcs150_date'] = datetime.strptime(date_text, fmt).isoformat()
                                break
                            except:
                                continue
                    except:
                        pass
        
        # Extract Power Units
        anchor = soup.find("a", string="Power Units:")
        if anchor:
            td = anchor.find_parent("th")
            if td:
                td = td.find_next_sibling("td")
                if td:
                    try:
                        data['power_units'] = int(td.text.strip().replace(",", ""))
                    except:
                        pass
        
        # Extract Drivers
        anchor = soup.find("a", string="Drivers:")
        if anchor:
            td = anchor.find_parent("th")
            if td:
                td = td.find_next_sibling("td")
                if td:
                    try:
                        data['drivers'] = int(td.text.strip().replace(",", ""))
                    except:
                        pass
        
        return data
        
    except Exception as e:
        return {"error": str(e)}


def calculate_authority_age_months(mcs150_date):
    """Calculate months since MCS-150 date (proxy for authority age)"""
    if not mcs150_date:
        return None
    try:
        date = datetime.fromisoformat(mcs150_date)
        diff = datetime.now() - date
        return int(diff.days / 30)
    except:
        return None


def score_lead(carrier_data):
    """
    Score a lead from 0-100 based on risk factors.
    Higher score = lower risk = better lead
    """
    data = load_data()
    weights = data.get("scoring_weights", {})
    
    score = 50  # Start at neutral
    breakdown = []
    
    # Authority Age scoring
    age_months = calculate_authority_age_months(carrier_data.get('mcs150_date'))
    if age_months is not None:
        age_weights = weights.get("authority_age_months", {})
        if age_months <= 6:
            delta = age_weights.get("0-6", -30)
            breakdown.append(f"Authority Age: {age_months}mo (🔴 Very New) {delta:+d}")
        elif age_months <= 12:
            delta = age_weights.get("6-12", -15)
            breakdown.append(f"Authority Age: {age_months}mo (🟠 New) {delta:+d}")
        elif age_months <= 24:
            delta = age_weights.get("12-24", 0)
            breakdown.append(f"Authority Age: {age_months}mo (🟡 Moderate) {delta:+d}")
        elif age_months <= 60:
            delta = age_weights.get("24-60", 10)
            breakdown.append(f"Authority Age: {age_months}mo (🟢 Established) {delta:+d}")
        else:
            delta = age_weights.get("60+", 20)
            breakdown.append(f"Authority Age: {age_months}mo (✅ Veteran) {delta:+d}")
        score += delta
    else:
        breakdown.append("Authority Age: Unknown (0)")
    
    # Safety Rating scoring
    rating = carrier_data.get('safety_rating', 'None')
    rating_weights = weights.get("safety_rating", {})
    delta = rating_weights.get(rating, 0)
    emoji = "✅" if rating == "Satisfactory" else "🟡" if rating == "None" else "🔴"
    breakdown.append(f"Safety Rating: {rating} ({emoji}) {delta:+d}")
    score += delta
    
    # Operating Status scoring
    status = carrier_data.get('status', 'Unknown')
    status_weights = weights.get("operating_status", {})
    delta = status_weights.get(status, 0)
    emoji = "✅" if status == "ACTIVE" else "🔴"
    breakdown.append(f"Operating Status: {status} ({emoji}) {delta:+d}")
    score += delta
    
    # Fleet Size bonus
    power_units = carrier_data.get('power_units', 0)
    if power_units >= 50:
        score += 15
        breakdown.append(f"Fleet Size: {power_units} trucks (✅ Large) +15")
    elif power_units >= 10:
        score += 10
        breakdown.append(f"Fleet Size: {power_units} trucks (🟢 Medium) +10")
    elif power_units >= 3:
        score += 5
        breakdown.append(f"Fleet Size: {power_units} trucks (🟡 Small) +5")
    else:
        breakdown.append(f"Fleet Size: {power_units} trucks (🟠 Owner-Op) +0")
    
    # Clamp score
    score = max(0, min(100, score))
    
    # Determine risk level
    thresholds = data.get("risk_thresholds", {"high_risk": 30, "medium_risk": 50, "low_risk": 70})
    if score < thresholds["high_risk"]:
        risk_level = "HIGH RISK"
        risk_emoji = "🔴"
    elif score < thresholds["medium_risk"]:
        risk_level = "MEDIUM RISK"
        risk_emoji = "🟠"
    elif score < thresholds["low_risk"]:
        risk_level = "LOW RISK"
        risk_emoji = "🟡"
    else:
        risk_level = "EXCELLENT"
        risk_emoji = "✅"
    
    return {
        "score": score,
        "risk_level": risk_level,
        "risk_emoji": risk_emoji,
        "breakdown": breakdown,
        "carrier_data": carrier_data,
        "scored_at": datetime.now().isoformat()
    }


def score_by_identifier(identifier, search_by_name=False):
    """Score a lead by MC, DOT number, or Name"""
    # Determine search type
    id_upper = identifier.upper().strip()
    
    if search_by_name:
        search_type = "Name"
        title_case_id = identifier.strip() # maintain casing for name
    else:
        if id_upper.startswith("DOT") or id_upper.startswith("USDOT"):
            # Extract number
            num = ''.join(filter(str.isdigit, id_upper))
            search_type = "USDOT"
            title_case_id = num
        elif id_upper.startswith("MC"):
            num = ''.join(filter(str.isdigit, id_upper))
            search_type = "MC_MX"
            title_case_id = num
        else:
            # Check if it looks like a number
            clean_num = ''.join(filter(str.isdigit, id_upper))
            if len(clean_num) > 4 and len(clean_num) == len(id_upper):
                title_case_id = clean_num
                # Try MC first (most common), fallback to DOT if not found
                search_type = "MC_MX"
            else:
                 # Assume name search if not a clear ID
                 search_type = "Name"
                 title_case_id = identifier.strip()
    
    carrier_data = get_carrier_info(title_case_id, search_type)
    
    # Fallback: If pure number search failed, try DOT (and vice versa)
    if "error" in carrier_data and search_type in ["MC_MX", "USDOT"]:
        fallback_type = "USDOT" if search_type == "MC_MX" else "MC_MX"
        carrier_data = get_carrier_info(title_case_id, fallback_type)
    
    if "error" in carrier_data:
        return {"error": carrier_data["error"]}
    
    result = score_lead(carrier_data)
    
    # Save to history
    data = load_data()
    data["score_history"].append({
        "identifier": identifier,
        "result": result
    })
    # Keep last 100 scores
    data["score_history"] = data["score_history"][-100:]
    save_data(data)
    
    return result


def get_score_history(limit=20):
    """Get recent score history"""
    data = load_data()
    return data.get("score_history", [])[-limit:]


def format_score_result(result):
    """Format score result for display"""
    if "error" in result:
        return f"❌ Error: {result['error']}"
    
    carrier = result.get("carrier_data", {})
    
    lines = [
        f"# {result['risk_emoji']} {result['risk_level']} - Score: {result['score']}/100",
        "",
        f"**Company:** {carrier.get('legal_name', 'Unknown')}",
    ]
    
    if carrier.get('dba_name'):
        lines.append(f"**DBA:** {carrier['dba_name']}")
    
    lines.extend([
        f"**DOT#:** {carrier.get('dot_number', 'N/A')}",
        f"**MC#:** {carrier.get('mc_number', 'N/A')}",
        "",
        "## Score Breakdown:",
    ])
    
    for item in result.get("breakdown", []):
        lines.append(f"- {item}")
    
    return "\n".join(lines)



# --- AI Integration ---
def analyze_risk_with_gemini(carrier_data):
    """
    Use Google Gemini to provide a deep-dive risk analysis of the carrier.
    """
    import sys
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from pocket_core.ai_helper import ask_gemini

    prompt = f"""
    You are a Freight Broker Risk Officer. Analyze this trucking company for fraud and safety risk.
    
    **Carrier Data:**
    - Legal Name: {carrier_data.get('legal_name', 'Unknown')}
    - DBA: {carrier_data.get('dba_name', 'N/A')}
    - MC Number: {carrier_data.get('mc_number', 'N/A')}
    - DOT Number: {carrier_data.get('dot_number', 'N/A')}
    - Safety Rating: {carrier_data.get('safety_rating', 'None')}
    - Operating Status: {carrier_data.get('status', 'Unknown')}
    - Fleet Size: {carrier_data.get('power_units', 0)} Trucks, {carrier_data.get('drivers', 0)} Drivers
    - Authority Age: {calculate_authority_age_months(carrier_data.get('mcs150_date'))} months active (Approx)
    
    **Task:**
    1. Give a "Verdict": [APPROVED], [CAUTION], or [DO NOT LOAD].
    2. Explain WHY in 3 bullet points.
    3. Identify specific "Red Flags" (e.g., specific age < 6 months, no inspections mentioned, conditional rating).
    4. Suggest 2 specific questions to ask the dispatcher to verify legitimacy.
    
    Keep it concise (under 200 words). Professional tone.
    """
    
    text, error = ask_gemini(prompt)
    if error:
        return f"⚠️ **AI Analysis Unavailable**: {error}"
    return text

if __name__ == "__main__":
    # Test
    import sys
    if len(sys.argv) > 1:
        result = score_by_identifier(sys.argv[1])
        print(format_score_result(result))
    else:
        print("Usage: python lead_manager.py MC123456")
