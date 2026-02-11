
import os
import shutil
import datetime
import zipfile

# CONFIG
PROJECT_ROOT = "/Volumes/CeeJay SSD/Projects/PocketEmpire"
BACKUP_DIR = "/Volumes/CeeJay SSD/Projects/PocketEmpire/Backups"
FOLDERS_TO_BACKUP = [
    "pocket_leads/data",
    "pocket_invoices",
    "pocket_credit"  # Added Credit module
]

def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    backup_name = f"Empire_Data_{timestamp}.zip"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    
    # Ensure backup dir exists
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    print(f"📦 Starting Backup: {timestamp}")
    
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in FOLDERS_TO_BACKUP:
            full_path = os.path.join(PROJECT_ROOT, folder)
            if os.path.exists(full_path):
                # Walk the folder and add files
                for root, dirs, files in os.walk(full_path):
                    for file in files:
                        # Skip .pyc, __pycache__, .DS_Store
                        if file.endswith('.pyc') or file == ".DS_Store" or "__pycache__" in root:
                            continue
                            
                        # Only backup JSON data, not code?
                        # Actually, backing up code is fine, but data is critical.
                        # Let's verify we are backing up JSONs specifically if needed.
                        # For invoices, 'invoices.json' is crit.
                        # For leads, 'lead_history.json'.
                        
                        file_path = os.path.join(root, file)
                        # Archive name relative to project root
                        arcname = os.path.relpath(file_path, PROJECT_ROOT)
                        zipf.write(file_path, arcname)
                        print(f"  + Added: {arcname}")
            else:
                print(f"⚠️ Warning: Folder not found: {folder}")
                
    print(f"✅ Backup Complete: {backup_path}")
    
    # Prune old backups (Keep last 7)
    cleanup_backups()

def cleanup_backups():
    backups = sorted([f for f in os.listdir(BACKUP_DIR) if f.startswith("Empire_Data_")])
    if len(backups) > 7:
        to_delete = backups[:-7]
        for f in to_delete:
            os.remove(os.path.join(BACKUP_DIR, f))
            print(f"🗑️ Pruned old backup: {f}")

if __name__ == "__main__":
    create_backup()
