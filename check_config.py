#!/usr/bin/env python3
import os
import sys
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIG ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
# Paths adjusted for where this script lives (root of PocketEmpire)
SERVICE_ACCOUNT_FILE = "/Volumes/CeeJay SSD/Projects/lead puller/service_account.json"
SHEET_NAME = "Lead Puller Master List"

def main():
    print("🚦 Checking Automation Status...")
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"⚠️ Warning: Service account not found at {SERVICE_ACCOUNT_FILE}")
        # Default to running if we can't check, otherwise we break the cron job entirely
        sys.exit(0) 

    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        client = gspread.authorize(creds)
        
        # Open Google Sheet
        try:
            sheet = client.open(SHEET_NAME)
        except Exception as e:
             print(f"⚠️ Could not find sheet '{SHEET_NAME}': {e}")
             sys.exit(0)

        # Check 'Config' Worksheet
        try:
            ws = sheet.worksheet("Config")
        except:
            # If Config sheet doesn't exist, we assume default is Active
            print("ℹ️ Config sheet not found. Defaulting to ACTIVE.")
            sys.exit(0)
            
        # Check Cell B2 (Value: "ACTIVE" or "PAUSED")
        # Structure: A2="Automation Status", B2="ACTIVE"
        val = ws.acell("B2").value
        status = str(val).strip().upper() if val else "ACTIVE"
        
        if status == "PAUSED":
            print("🛑 GLOBAL STOP: Automation is PAUSED in Google Sheets.")
            sys.exit(1) # Exit Code 1 stops the bash script
        else:
            print(f"✅ Status is '{status}'. Proceeding.")
            sys.exit(0) # Exit Code 0 allows execution
            
    except Exception as e:
        print(f"⚠️ Config Check Error: {e}. Defaulting to ACTIVE.")
        sys.exit(0)

if __name__ == "__main__":
    main()
