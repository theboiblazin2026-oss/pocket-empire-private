import requests
from bs4 import BeautifulSoup
import time
import random

import os

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)
MONITORED_MCS_FILE = os.path.join(PROJECT_ROOT, "monitored_mcs.txt")

def get_carrier_status(identifier, search_type="MC_MX"):
    """
    Scrapes SAFER for a single MC/DOT.
    identifier: The number (MC or DOT)
    search_type: "MC_MX" or "USDOT"
    """
    
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    
    try:
        # SAFER Search Logic (POST is required for robustness)
        url = "https://safer.fmcsa.dot.gov/query.asp"
        payload = {
            "searchtype": "ANY",
            "query_type": "queryCarrierSnapshot",
            "query_param": search_type, # MC_MX or USDOT
            "query_string": identifier.strip()
        }
        
        # print(f"DEBUG: Posting to {url} with {payload}")
        r = s.post(url, data=payload, timeout=15)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Check if found (Title usually contains "Company Snapshot")
        if "Company Snapshot" not in r.text or "Record Not Found" in r.text:
             return {"error": "Not Found / Invalid ID"}

        data = {
            "legal_name": "Unknown",
            "status": "Unknown",
            "rating": "None"
        }
        
        # SAFER puts labels inside <a class="querylabel"> tags
        # We need to find those anchor tags and then get the next <td>
        
        # Extract Legal Name
        for label in ["Legal Name:", "Name:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                # The value is in the next <td> after the parent <th>
                td = anchor.find_parent("th").find_next_sibling("td")
                if td:
                    data['legal_name'] = td.text.strip()
                    break
                    
        # Extract USDOT Status
        for label in ["USDOT Status:", "Operating Status:", "Status:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                td = anchor.find_parent("th").find_next_sibling("td")
                if td:
                    val = td.text.strip()
                    # Clean up any HTML comments or extra whitespace
                    if "ACTIVE" in val.upper():
                        data['status'] = "ACTIVE"
                    elif "INACTIVE" in val.upper():
                        data['status'] = "INACTIVE"
                    elif "OUT-OF-SERVICE" in val.upper() or "OUT OF SERVICE" in val.upper():
                        data['status'] = "OUT-OF-SERVICE"
                    else:
                        data['status'] = val
                    break
                    
        # Extract Safety Rating
        for label in ["Safety Rating:", "Rating:"]:
            anchor = soup.find("a", string=label)
            if anchor:
                td = anchor.find_parent("th").find_next_sibling("td")
                if td:
                    val = td.text.strip()
                    if "Rating Date" in val:
                        val = val.split(":")[0].strip()
                    data['rating'] = val
                    break
            
        return data

    except Exception as e:
        return {"error": str(e)}

def get_monitored_mcs(file_path=MONITORED_MCS_FILE):
    """Read monitored list, supporting 'ID|Alias' format."""
    if not os.path.exists(file_path):
        return []
    
    entries = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                # Parse "DOT:12345|My Trucking Co"
                parts = line.split('|')
                identifier = parts[0].strip()
                alias = parts[1].strip() if len(parts) > 1 else None
                
                entries.append({
                    "id": identifier,
                    "alias": alias,
                    "raw": line
                })
    return entries

def add_mc(mc_number, alias=None):
    """Add a new MC/DOT to the list with optional alias."""
    current = get_monitored_mcs()
    # Check for duplicates (by ID)
    if any(e['id'] == mc_number for e in current):
        return False
    
    line = f"{mc_number}|{alias}" if alias else mc_number
    
    with open(MONITORED_MCS_FILE, 'a') as f:
        f.write(f"{line}\n")
    return True

def remove_mc(raw_line_or_id):
    """Remove an entry by its ID or raw line content."""
    current = get_monitored_mcs()
    target_id = raw_line_or_id.split("|")[0].strip() if "|" in raw_line_or_id else raw_line_or_id
    
    new_entries = []
    found = False
    
    for entry in current:
        # Check by ID (more robust than raw line match)
        if entry['id'] == target_id:
            found = True
            continue 
        new_entries.append(entry['raw'])
        
    if found:
        with open(MONITORED_MCS_FILE, 'w') as f:
            for line in new_entries:
                f.write(f"{line}\n")
        return True
    return False

if __name__ == "__main__":
    # Test with a known MC
    print(get_carrier_status("123456")) # Invalid
    # Provide a real test MC execution manually if needed
