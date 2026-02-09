import os
import shutil
import glob

# Paths
PROJECTS_ROOT = "/Volumes/CeeJay SSD/Projects"
POCKET_EMPIRE_DIR = os.path.join(PROJECTS_ROOT, "PocketEmpire")
APPS_BUILDS_DIR = os.path.join(POCKET_EMPIRE_DIR, "apps_builds")
ARCHIVE_DIR = os.path.join(PROJECTS_ROOT, "_Archive")

def safe_move(src, dst):
    try:
        if not os.path.exists(src):
            print(f"Source not found: {src}")
            return
        if not os.path.exists(dst):
            os.makedirs(dst, exist_ok=True)
            print(f"Created directory: {dst}")
        
        # If dst is a directory, move src inside it
        # If src is a directory and dst is a directory, move src *into* dst
        # We want to move contents of PocketEmpire_Apps to apps_builds
        
        print(f"Moving {src} to {dst}")
        shutil.move(src, dst)
        print("Success")
    except Exception as e:
        print(f"Error moving {src} to {dst}: {e}")

def organize_contents():
    # 1. Pocket Empire Apps
    pe_apps = os.path.join(PROJECTS_ROOT, "PocketEmpire_Apps")
    if os.path.exists(pe_apps):
        os.makedirs(APPS_BUILDS_DIR, exist_ok=True)
        # Move inner contents
        for item in os.listdir(pe_apps):
            s = os.path.join(pe_apps, item)
            d = os.path.join(APPS_BUILDS_DIR, item)
            if os.path.exists(d):
                print(f"Destination exists, skipping: {d}")
            else:
                shutil.move(s, d)
        # Remove empty dir
        try:
            os.rmdir(pe_apps)
        except OSError:
            print(f"Could not remove {pe_apps}, might not be empty")

    # 2. Archive Directory
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    # 3. Dispatch App Swap
    # Goal: 
    #   Current "Dispatch App" -> "_Archive/Dispatch App (Old)"
    #   "Dispatch App (Migrated Snapshot)" -> "Dispatch App"
    
    current_dispatch = os.path.join(PROJECTS_ROOT, "Dispatch App")
    snapshot_dispatch = os.path.join(PROJECTS_ROOT, "Dispatch App (Migrated Snapshot)")
    archive_dispatch = os.path.join(ARCHIVE_DIR, "Dispatch App (Old)")
    
    if os.path.exists(snapshot_dispatch):
        if os.path.exists(current_dispatch):
            print("Archiving current Dispatch App...")
            shutil.move(current_dispatch, archive_dispatch)
        
        print("Restoring Snapshot to Dispatch App...")
        shutil.move(snapshot_dispatch, current_dispatch)

    # 4. Archive other folders
    to_archive = [
        "Dispatch (Old)",
        "Infinite-Bond-Memorials (Migrated 1769958852)",
        "Infinite-Bond-Memorials (Migrated Snapshot)",
        "Jayboi_Services_Site (Migrated 1769958852)",
        "Jayboi_Services_Site (Migrated Snapshot)",
        "Truck Scraper Master File (Migrated 1769958852)",
        "Truck Scraper Master File (Migrated Snapshot)",
        "lead puller (Migrated Snapshot)",
        "Tech Trap Solutions (Migrated Snapshot)", # Archiving the snapshot as per plan if not used, or check logic?
        # Plan said: Compare Tech Trap. Current had only minimal package.json. Snapshot didn't exist in my view_file attempt (error).
        # Actually I failed to read snapshot package.json. Let's just archive the snapshot if it exists for now to clean root.
    ]
    
    for folder in to_archive:
        src = os.path.join(PROJECTS_ROOT, folder)
        if os.path.exists(src):
            dst = os.path.join(ARCHIVE_DIR, folder)
            if os.path.exists(dst):
                print(f"Archive destination exists: {dst}, skipping move")
            else:
                shutil.move(src, dst)

    # 5. Archive loose python scripts in root
    # Be careful not to move this script if it was in root, but it's in PocketEmpire/scripts
    for file in os.listdir(PROJECTS_ROOT):
        if file.endswith(".py") and os.path.isfile(os.path.join(PROJECTS_ROOT, file)):
             # Don't move if it's a specific important script? Assuming all loose .py are clutter
             shutil.move(os.path.join(PROJECTS_ROOT, file), os.path.join(ARCHIVE_DIR, file))

if __name__ == "__main__":
    organize_contents()
