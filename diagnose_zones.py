
import os

def is_backup_location(path):
    backup_markers = [
        '/HDD_Import_',
        '/desktop_migrated',
        '/downloads_migrated',
        '/library_caches_migrated'
    ]
    return any(marker in path for marker in backup_markers)

def is_protected_zone(path):
    protected_markers = [
        '/Volumes/CeeJay SSD/Documents',
        '/Volumes/CeeJay SSD/Projects',
        '/Volumes/CeeJay SSD/Movies',
        '/Volumes/CeeJay SSD/Music',
        '/Volumes/CeeJay SSD/Pictures',
        '/Users/newguy/Documents',
        '/Users/newguy/Projects'
    ]
    return any(marker in path for marker in protected_markers)

def diagnose_missing_zones(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    sets = []
    current_set = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("Set"):
            if current_set:
                sets.append(current_set)
            current_set = []
        elif line.startswith("- /"):
            current_set.append(line[2:])

    if current_set:
        sets.append(current_set)

    missing_zones = {}
    
    for group in sets:
        backup_copies = [p for p in group if is_backup_location(p)]
        real_copies = [p for p in group if not is_backup_location(p)]
        
        if backup_copies and real_copies:
            # This is a safe deletion in V2.
            # Check if it was failed in Paranoid due to Protected Zone mismatch.
            protected_copies = [p for p in group if is_protected_zone(p)]
            
            if not protected_copies:
                # Found a gap! The 'real' copy is in a folder we didn't whitelist.
                for real_path in real_copies:
                    folder = os.path.dirname(real_path)
                    # Get top level folder for cleaner stats
                    parts = real_path.split(os.sep)
                    if len(parts) > 3:
                        top_folder = os.sep.join(parts[:4])
                    else:
                        top_folder = folder
                    
                    try:
                        size = os.path.getsize(real_path)
                    except: 
                        size = 0
                        
                    missing_zones[top_folder] = missing_zones.get(top_folder, 0) + size

    print("Folders containing 'Master' copies that were excluded from Protected Zone:")
    for folder, size in sorted(missing_zones.items(), key=lambda x: x[1], reverse=True):
         print(f"  - {folder}: {size / (1024*1024):.2f} MB")

if __name__ == "__main__":
    diagnose_missing_zones("duplicates_report.txt")
