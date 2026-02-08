import sys
import os

# Initialize path to find pocket_core
sys.path.append("/Volumes/CeeJay SSD/Projects/PocketEmpire")

from pocket_core.db import get_db

def check_tables():
    print("🔌 Connecting to Supabase...")
    db = get_db()
    
    if not db:
        print("❌ Could not connect to Supabase. Check env vars or secrets.")
        return

    print("✅ Connection Object Created.")
    
    # Check Inspections Table
    print("\n🔍 Checking 'inspections' table...")
    try:
        # Try to select 1 row just to see if table exists
        response = db.table("inspections").select("id").limit(1).execute()
        print("✅ 'inspections' table EXISTS and is accessible.")
        print(f"   (Found {len(response.data)} rows)")
    except Exception as e:
        print("❌ 'inspections' table INVALID or MISSING.")
        print(f"   Error: {e}")
        print("\n👉 DID YOU RUN THE SQL? Go to Supabase SQL Editor and run the script I provided.")

    # Check News Feeds
    print("\n🔍 Checking 'feeds.json' (News Curator)...")
    feed_path = "/Volumes/CeeJay SSD/Projects/PocketEmpire/pocket_news/feeds.json"
    if os.path.exists(feed_path):
        print(f"✅ 'feeds.json' found at {feed_path}")
        with open(feed_path, 'r') as f:
            print(f"   Content snippet: {f.read()[:100]}...")
    else:
        print("❌ 'feeds.json' NOT FOUND.")

if __name__ == "__main__":
    check_tables()
