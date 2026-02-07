import os
import sys

# Add current dir to path to find pocket_core
sys.path.append(os.getcwd())

from pocket_core import db

def test_conn():
    print("🔌 Testing Supabase Connection...")
    client = db.get_db()
    
    if not client:
        print("❌ Could not initialize client. Check secrets.toml format.")
        return
    
    try:
        # Try a simple read (even if table empty, it should not auth error)
        # valid table from our schema is 'company_settings' or 'leads'
        res = client.table("company_settings").select("*").limit(1).execute()
        print(f"✅ Connection Successful! Response: {res}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_conn()
