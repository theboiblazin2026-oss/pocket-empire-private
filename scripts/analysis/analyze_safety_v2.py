
import os

def is_backup_location(path):
    # These are definitely backups/transient
    backup_markers = [
        '/HDD_Import_',
        '/desktop_migrated',
        '/downloads_migrated',
        '/library_caches_migrated',
        '/.Trash',
        '/Recycled'
    ]
    return any(marker in path for marker in backup_markers)

def is_app_garbage(path):
    garbage_markers = [
        '.app/',
        'node_modules',
        'venv/',
        '.git/',
        'stable-diffusion-forge',
        'site-packages',
        'Library/Caches'
    ]
    return any(marker in path for marker in garbage_markers)

def analyze_safety_v2(filename):
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
            current_set.append(line[2:]) # remove "- "

    if current_set:
        sets.append(current_set)

    safe_count = 0
    safe_size = 0
    
    potential_safe_count = 0 
    potential_safe_size = 0

    sources = {}

    for group in sets:
        path = group[0]
        try:
            size_per_file = os.path.getsize(path)
        except:
            size_per_file = 0

        # Categorize every file in the group
        # 1. Is it inside a backup folder?
        backup_copies = [p for p in group if is_backup_location(p)]
        
        # 2. Is it elsewhere (ANYWHERE else that is not a backup folder)?
        # real_copies list contains paths that are NOT in backup folders.
        real_copies = [p for p in group if not is_backup_location(p)]

        if len(real_copies) > 0 and len(backup_copies) > 0:
            # We have at least one Real copy and at least one Backup copy.
            # The Backup copies are SAFE TO DELETE.
            safe_count += len(backup_copies)
            safe_size += len(backup_copies) * size_per_file
            
            for p in backup_copies:
                folder = "Other Import"
                if "HDD_Import" in p: folder = "HDD_Import"
                elif "desktop_migrated" in p: folder = "desktop_migrated"
                elif "downloads_migrated" in p: folder = "downloads_migrated"
                sources[folder] = sources.get(folder, 0) + size_per_file

        elif len(real_copies) == 0:
            # All copies are in backup folders! (e.g. HDD_Import vs desktop_migrated)
            # We can technically delete all but one, but which one?
            # It's "Potentially Safe" to consolidate.
            if len(group) > 1:
                potential_safe_count += len(group) - 1
                potential_safe_size += (len(group) - 1) * size_per_file

    print(f"Safety Analysis Results (V2 - Broader Logic):")
    print(f"Total Duplicates Analyzed: {len(sets)} sets")
    print("-" * 30)
    print(f"CONFIRMED SAFE TO REMOVE:")
    print(f"criterion: File exists in a regular folder AND in a backup folder.")
    print(f"  Files: {safe_count}")
    print(f"  Space: {safe_size / (1024*1024*1024):.2f} GB")
    print("\n  Sources of Safe Deletions:")
    for source, size in sources.items():
        print(f"    - {source}: {size / (1024*1024*1024):.2f} GB")
    
    print("-" * 30)
    print(f"POTENTIAL CONSOLIDATION (All copies are in Backups):")
    print(f"criterion: File exists ONLY in various backup folders (e.g. Import vs Migrated).")
    print(f"  Files: {potential_safe_count}")
    print(f"  Space: {potential_safe_size / (1024*1024*1024):.2f} GB")

if __name__ == "__main__":
    analyze_safety_v2("duplicates_report.txt")
