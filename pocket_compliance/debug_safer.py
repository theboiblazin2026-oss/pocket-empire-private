import requests
from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

s = requests.Session()
s.headers.update({"User-Agent": USER_AGENT})

# Test with the DOT from screenshot
dot = "3973577"
url = "https://safer.fmcsa.dot.gov/query.asp"
payload = {
    "searchtype": "ANY",
    "query_type": "queryCarrierSnapshot",
    "query_param": "USDOT",
    "query_string": dot
}

print(f"Fetching {url} with POST...")
r = s.post(url, data=payload, timeout=15)
print(f"Status: {r.status_code}")

# Dump raw to see what we got
with open("safer_debug.html", "w") as f:
    f.write(r.text)

# Try parse
soup = BeautifulSoup(r.text, 'html.parser')

# New approach: find anchor tags
name_anchor = soup.find("a", string="Legal Name:")
if name_anchor:
    td = name_anchor.find_parent("th").find_next_sibling("td")
    print(f"Legal Name Found: {td.text.strip()}")
else:
    print("❌ Legal Name Anchor NOT Found")

status_anchor = soup.find("a", string="USDOT Status:")
if status_anchor:
    td = status_anchor.find_parent("th").find_next_sibling("td")
    print(f"USDOT Status Found: {td.text.strip()}")
else:
    print("❌ USDOT Status Anchor NOT Found")
