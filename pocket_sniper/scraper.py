import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.json")
FINDS_FILE = os.path.join(DATA_DIR, "finds.json")

# User Agents to rotate (Basic list)
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0"
]

def load_json(filepath, default=[]):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def search_craigslist(city, query, min_price=None, max_price=None):
    """
    Search Craigslist for a query.
    Returns list of dicts: {title, price, url, image_url, date}
    """
    base_url = f"https://{city}.craigslist.org/search/sss"
    params = {
        "query": query,
        "sort": "date" # Newest first
    }
    if min_price: params["min_price"] = min_price
    if max_price: params["max_price"] = max_price

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
    }

    print(f"🔎 Searching {city} for: {query}...")
    
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # CL structure changes, but usually .cl-static-search-result or .result-row
    # Modern CL often uses <li class="cl-static-search-result" ...> or <li class="result-row">
    # Let's try flexible parsing
    
    rows = soup.find_all("li", class_="cl-static-search-result")
    if not rows:
        rows = soup.find_all("li", class_="result-row") # fallback to old class

    for row in rows:
        try:
            # Title & Link
            title_el = row.find("div", class_="title") or row.find("a", class_="result-title")
            if not title_el: continue
            
            title = title_el.text.strip()
            link = title_el.get("href") or row.find("a")["href"]
            
            # Price
            price_el = row.find("div", class_="price") or row.find("span", class_="result-price")
            price = price_el.text.strip() if price_el else "$?"
            
            # ID
            pid = row.get("data-pid") or link.split('/')[-1].replace('.html', '')
            
            # Location
            loc_el = row.find("div", class_="location") or row.find("span", class_="result-hood")
            location = loc_el.text.strip() if loc_el else city

            results.append({
                "id": pid,
                "title": title,
                "price": price,
                "link": link,
                "location": location,
                "city": city,
                "found_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "query": query,
                "read": False
            })
        except Exception as e:
            continue
            
    return results

def run_sniper():
    """Run all alerts and update fines"""
    alerts = load_json(ALERTS_FILE)
    if not alerts:
        return "No alerts configured."

    current_finds = load_json(FINDS_FILE)
    existing_ids = set(item['id'] for item in current_finds)
    
    new_count = 0
    
    for alert in alerts:
        if not alert.get('active', True):
            continue
            
        # Add random sleep to be nice
        time.sleep(random.uniform(2, 5))
        
        results = search_craigslist(
            alert.get('city', 'newyork'),
            alert['keyword'],
            alert.get('min_price'),
            alert.get('max_price')
        )
        
        for res in results:
            if res['id'] not in existing_ids:
                current_finds.insert(0, res) # Add to top
                existing_ids.add(res['id'])
                new_count += 1
                
    # Save back
    save_json(FINDS_FILE, current_finds[:500]) # Keep last 500
    return f"Scan complete. Found {new_count} new items."

if __name__ == "__main__":
    print(run_sniper())
