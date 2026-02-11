#!/usr/bin/env python3
"""
☁️  Pocket Empire — Cloud Sync
Pushes all local JSON data to Supabase so the app works on Streamlit Cloud / tablet.
Run:  python3 scripts/cloud_sync.py
"""
import json, os, sys, toml
from datetime import datetime

# Path setup
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from supabase import create_client

# --- Config: All files to sync ---
SYNC_MAP = {
    "invoices_data":      "pocket_invoices/invoices.json",
    "leads_data":         "pocket_leads/leads.json",
    "leads_history":      "pocket_leads/data/lead_history.json",
    "dispatch_loads":     "pocket_leads/data/dispatch_loads.json",
    "credit_clients":     "pocket_credit/clients.json",
    "personal_credit":    "pocket_credit/personal_credit.json",
    "compliance_history": "pocket_compliance/history.json",
    "reminders":          "pocket_reminders/reminders.json",
    "sniper_alerts":      "pocket_sniper/data/alerts.json",
    "sniper_finds":       "pocket_sniper/data/finds.json",
    "rates_data":         "pocket_rates/rates.json",
    "news_feeds":         "pocket_news/feeds.json",
    "router_data":        "pocket_router/router.json",
}


def get_client():
    """Connect to Supabase using secrets.toml."""
    secrets_path = os.path.join(ROOT, ".streamlit", "secrets.toml")
    if not os.path.exists(secrets_path):
        print("❌ .streamlit/secrets.toml not found")
        sys.exit(1)
    secrets = toml.load(secrets_path)
    url = secrets.get("SUPABASE_URL", "")
    key = secrets.get("SUPABASE_KEY", "")
    if not url or not key:
        print("❌ SUPABASE_URL or SUPABASE_KEY missing from secrets.toml")
        sys.exit(1)
    return create_client(url, key)


def sync_json(client, key, rel_path, label):
    """Upsert a single JSON file into app_data."""
    filepath = os.path.join(ROOT, rel_path)
    if not os.path.exists(filepath):
        print(f"  ⏭️  {label}: not found, skipping")
        return False
    try:
        with open(filepath) as f:
            data = json.load(f)
        size = len(json.dumps(data))
        client.table("app_data").upsert({
            "key": key,
            "value": data,
            "updated_at": datetime.utcnow().isoformat()
        }).execute()
        print(f"  ✅ {label}: synced ({size:,} bytes)")
        return True
    except Exception as e:
        print(f"  ❌ {label}: {e}")
        return False


def sync_wealth(client):
    """Sync all wealth profiles."""
    wealth_dir = os.path.join(ROOT, "pocket_wealth", "data")
    if not os.path.isdir(wealth_dir):
        return 0
    count = 0
    for fn in os.listdir(wealth_dir):
        if fn.endswith("_wealth.json"):
            name = fn.replace("_wealth.json", "")
            if sync_json(client, f"wealth_{name}", f"pocket_wealth/data/{fn}", f"Wealth: {name}"):
                count += 1
    return count


def main():
    print("=" * 60)
    print(f"☁️  POCKET EMPIRE — CLOUD SYNC")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    client = get_client()

    # Test connection
    try:
        client.table("app_data").select("key").limit(1).execute()
        print("🔌 Supabase: Connected ✅\n")
    except Exception as e:
        print(f"🔌 Supabase: Connection FAILED ❌ — {e}")
        sys.exit(1)

    # Sync modules
    ok = 0
    print("📦 Syncing Module Data:")
    for key, path in SYNC_MAP.items():
        label = key.replace("_", " ").title()
        if sync_json(client, key, path, label):
            ok += 1

    # Sync wealth
    print("\n💰 Syncing Wealth Profiles:")
    ok += sync_wealth(client)

    # Report
    print("\n" + "=" * 60)
    rows = client.table("app_data").select("key, updated_at").execute()
    print(f"📊 Total items in cloud: {len(rows.data)}")
    for row in sorted(rows.data, key=lambda x: x["key"]):
        ts = row["updated_at"][:19].replace("T", " ")
        print(f"   📁 {row['key']:30s} | {ts}")
    print(f"\n✨ Done — {ok} modules synced successfully!")


if __name__ == "__main__":
    main()
