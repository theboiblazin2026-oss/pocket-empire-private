import gspread
from google.oauth2.service_account import Credentials
import toml
import os
import sys

# Setup Paths
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
secrets_path = os.path.join(root_dir, ".streamlit", "secrets.toml")

# Auth Scopes
SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def get_client(service_account_info):
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    return gspread.authorize(creds)

def migrate_sheet(client, sheet_name_or_key, worksheet_name, new_cols):
    try:
        if sheet_name_or_key.startswith("1") and len(sheet_name_or_key) > 20:
             sh = client.open_by_key(sheet_name_or_key)
        else:
             sh = client.open(sheet_name_or_key)
        
        try:
            ws = sh.worksheet(worksheet_name)
        except:
            ws = sh.sheet1 # Fallback
            
        headers = ws.row_values(1)
        print(f"Checking {sh.title} - {ws.title}...")
        
        added = 0
        for col in new_cols:
            if col not in headers:
                print(f"  + Adding column: {col}")
                # Update cell (1, len+1)
                ws.update_cell(1, len(headers) + 1 + added, col)
                added += 1
            else:
                print(f"  - Column exists: {col}")
                
        if added > 0:
            print(f"✅ Added {added} new columns to {sh.title}")
        else:
            print(f"✅ {sh.title} is already up to date.")
            
    except Exception as e:
        print(f"❌ Error migrating {sheet_name_or_key}: {e}")

def main():
    print("🚀 Starting Phase 16 Database Migration...")
    
    if not os.path.exists(secrets_path):
        print("❌ secrets.toml not found!")
        return

    secrets = toml.load(secrets_path)
    
    # 1. Web Hunter Migration
    if "web_hunter" in secrets:
        print("\n--- Migrating Web Hunter ---")
        conf = secrets["web_hunter"]
        if "gcp_service_account" in conf:
            client = get_client(dict(conf["gcp_service_account"]))
            sheet_name = conf.get("sheet_name", "Lead Puller Master List")
            ws_name = conf.get("worksheet_name", "Website Leads")
            
            # Add Drip Columns
            new_cols = ["Campaign Stage", "Next Action", "Sequence ID", "Last Email Subject"]
            migrate_sheet(client, sheet_name, ws_name, new_cols)

    # 2. Fleet Manager Migration
    if "fleet_manager" in secrets:
        print("\n--- Migrating Fleet Manager ---")
        conf = secrets["fleet_manager"]
        if "gcp_service_account" in conf:
            client = get_client(dict(conf["gcp_service_account"]))
            sheet_id = conf.get("sheet_id")
            
            # Add Drip Columns
            new_cols = ["Campaign Stage", "Next Action", "Sequence ID", "Last Email Subject"]
            migrate_sheet(client, sheet_id, "Sheet1", new_cols)

    print("\n✨ Migration Complete!")

if __name__ == "__main__":
    main()
