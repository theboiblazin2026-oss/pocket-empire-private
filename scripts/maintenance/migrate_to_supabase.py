import json
import os
import sys

# Ensure we can import pocket_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from pocket_core import db

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def migrate_invoices():
    print("🧾 Migrating Invoices...")
    path = os.path.join(os.path.dirname(__file__), "pocket_invoices/invoices.json")
    data = load_json(path)
    if not data:
        print("   No local invoices.json found.")
        return

    client = db.get_db()
    if not client:
        print("   ❌ No DB Connection.")
        return

    invoices = data.get("invoices", [])
    count = 0
    for inv in invoices:
        try:
            # Flatten details for SQL
            details = inv.get("details", {})
            payload = {
                "id": inv.get("id"),
                "client_name": inv.get("client"),
                "amount": inv.get("amount"),
                "status": inv.get("status"),
                "origin": details.get("origin"),
                "destination": details.get("dest"),
                "load_ref": details.get("ref"),
                "data": inv # Store full object!
            }
            client.table("invoices").upsert(payload).execute()
            count += 1
        except Exception as e:
            print(f"   ⚠️ Failed to migrate {inv.get('id')}: {e}")
            
    print(f"   ✅ Migrated {count} invoices.")

    print(f"   ✅ Migrated {count} invoices.")

def migrate_app_data():
    print("💾 Migrating App Data (Wealth & Leads)...")
    client = db.get_db()
    if not client: return

    # 1. Leads History
    leads_path = os.path.join(os.path.dirname(__file__), "pocket_leads/leads.json")
    leads_data = load_json(leads_path)
    if leads_data:
        try:
            client.table("app_data").upsert({
                "key": "leads_history",
                "value": leads_data,
                "updated_at": "now()"
            }).execute()
            print("   ✅ Migrated Leads History")
        except Exception as e:
            print(f"   ⚠️ Failed to migrate Leads: {e}")

    # 2. Wealth Data (Find all profiles)
    wealth_dir = os.path.join(os.path.dirname(__file__), "pocket_wealth/data")
    if os.path.exists(wealth_dir):
        for filename in os.listdir(wealth_dir):
            if filename.endswith("_wealth.json"):
                # Extract client name from filename if possible, or just use filename as key suffix
                # Client Key logic in manager is: f"wealth_{client_name}"
                # Filename is: f"{safe_name}_wealth.json"
                # safe_name is what we use in key? 
                # Actually manager uses client_name to generate filename.
                # But when loading, we might need the original name? 
                # Let's just use the filename prefix as the unique identifier for now.
                # Wait, the manager uses `client_name` to geneate key `wealth_{client_name}`.
                # If I only have the filename `myself_wealth.json`, safely `myself` is the key suffix.
                
                safe_name = filename.replace("_wealth.json", "")
                key = f"wealth_{safe_name}"
                
                data = load_json(os.path.join(wealth_dir, filename))
                if data:
                    try:
                        client.table("app_data").upsert({
                            "key": key,
                            "value": data,
                            "updated_at": "now()"
                        }).execute()
                        print(f"   ✅ Migrated Wealth Profile: {safe_name}")
                    except Exception as e:
                        print(f"   ⚠️ Failed to migrate Wealth {safe_name}: {e}")

def main():
    print("🚀 Starting Migration to Supabase...")
    if not db.get_db():
        print("❌ Supabase not configured in secrets.toml.")
        print("   Please add SUPABASE_URL and SUPABASE_KEY to .streamlit/secrets.toml")
        return

    migrate_invoices()
    migrate_app_data()
    print("✨ Migration Complete!")

if __name__ == "__main__":
    main()
