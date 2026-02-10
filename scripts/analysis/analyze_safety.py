
import os

def is_keep_location(path):
    # Primary user folders where data SHOULD live
    keep_markers = [
        '/Volumes/CeeJay SSD/Documents',
        '/Volumes/CeeJay SSD/Projects',
        '/Volumes/CeeJay SSD/Movies',
        '/Volumes/CeeJay SSD/Music',
        '/Volumes/CeeJay SSD/Pictures',
        '/Users/newguy/Documents',
        '/Users/newguy/Projects'
    ]
    return any(marker in path for marker in keep_markers)

def is_discard_location(path):
    # Folders that look like temporary backups or imports
    discard_markers = [
        'HDD_Import_20260131',
        'desktop_migrated',
        'downloads_migrated',
        'library_caches_migrated',
        '/Downloads/'
    ]
    return any(marker in path for marker in discard_markers)

def is_app_garbage(path):
    # Files that are likely app internals and shouldn't be touched manually
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

def analyze_safety(filename):
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
    
    unsafe_count = 0
    unsafe_size = 0
    
    manual_review_count = 0
    manual_review_size = 0

    discard_sources = {} 

    for group in sets:
        path = group[0]
        try:
            size_per_file = os.path.getsize(path)
        except:
            size_per_file = 0

        keep_copies = [p for p in group if is_keep_location(p)]
        discard_copies = [p for p in group if is_discard_location(p)]
        app_garbage = [p for p in group if is_app_garbage(p)]

        if len(keep_copies) > 0:
            # We have at least one GOOD copy. All discard copies are safe to remove.
            # IMPORTANT: Are we sure we aren't deleting something we shouldn't?
            # If a file is in 'discard_copies' it matched the discard markers.
            
            # Filter out any discard copies that are technically "keep" copies (overlap?)
            # The logic above separates them, but let's be sure.
            
            actual_removals = [p for p in discard_copies if p not in keep_copies]
            
            if actual_removals:
                safe_count += len(actual_removals)
                safe_size += len(actual_removals) * size_per_file
                
                # Track where these are coming from
                for p in actual_removals:
                    folder = "Other"
                    if "HDD_Import" in p: folder = "HDD_Import"
                    elif "desktop_migrated" in p: folder = "desktop_migrated"
                    elif "downloads_migrated" in p: folder = "downloads_migrated"
                    
                    discard_sources[folder] = discard_sources.get(folder, 0) + size_per_file
        else:
            # No copy in a "Keep" location. 
            if len(app_garbage) == len(group):
                # All copies are app garbage.
                unsafe_count += len(group) - 1 # effectively duplicated garbage
                unsafe_size += (len(group) - 1) * size_per_file
            else:
                # Copies exist but none are in definitive "Keep" folders. 
                # (e.g. one in HDD_Import, one in desktop_migrated).
                manual_review_count += len(group)
                manual_review_size += (len(group)-1) * size_per_file

    print(f"Safety Analysis Results:")
    print(f"Total Duplicates Analyzed: {len(sets)} sets")
    print("-" * 30)
    print(f"SAFE TO REMOVE (Redundant Migration Files):")
    print(f"  Files: {safe_count}")
    print(f"  Space: {safe_size / (1024*1024*1024):.2f} GB")
    print("\n  Sources of Safe Deletions:")
    for source, size in discard_sources.items():
        print(f"    - {source}: {size / (1024*1024*1024):.2f} GB")
    
    print("-" * 30)
    print(f"APP/SYSTEM GARBAGE (Leave Alone):")
    print(f"  Files: {unsafe_count}")
    print(f"  Space: {unsafe_size / (1024*1024*1024):.2f} GB")
    
    print("-" * 30)
    print(f"MANUAL REVIEW NEEDED (No 'Main' Copy Found):")
    print(f"  Files: {manual_review_count}")
    print(f"  Space: {manual_review_size / (1024*1024*1024):.2f} GB")

if __name__ == "__main__":
    analyze_safety("duplicates_report.txt")
