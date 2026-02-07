
import os
from collections import defaultdict

def scan_leftovers():
    # Targets to analyze
    targets = [
        '/Volumes/CeeJay SSD/HDD_Import_20260131',
        '/Volumes/CeeJay SSD/desktop_migrated',
        '/Volumes/CeeJay SSD/downloads_migrated'
    ]

    print("Scanning leftover files in migration folders...")
    
    stats = defaultdict(lambda: {'count': 0, 'size': 0})
    file_types = defaultdict(int)
    
    empty_dirs = 0
    total_files = 0
    total_size = 0

    for target in targets:
        if not os.path.exists(target):
            print(f"Target not found: {target}")
            continue
            
        target_name = os.path.basename(target)
        
        for root, dirs, files in os.walk(target, topdown=False):
            # topdown=False so we can count empty dirs effectively if needed
            
            for f in files:
                if f == ".DS_Store": continue
                
                path = os.path.join(root, f)
                try:
                    size = os.path.getsize(path)
                    stats[target_name]['count'] += 1
                    stats[target_name]['size'] += size
                    
                    ext = os.path.splitext(f)[1].lower()
                    file_types[ext] += 1
                    
                    total_files += 1
                    total_size += size
                except:
                    pass

            if not os.listdir(root):
                empty_dirs += 1

    print("\nLeftover Analysis Report")
    print("========================")
    print(f"Total Files Remaining: {total_files}")
    print(f"Total Size Remaining: {total_size / (1024*1024*1024):.2f} GB")
    print(f"Empty Directories Found: {empty_dirs}")
    
    print("\nBreakdown by Folder:")
    for folder, data in stats.items():
        print(f"  - {folder}: {data['count']} files ({data['size'] / (1024*1024*1024):.2f} GB)")
        
    print("\nTop File Types:")
    sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]
    for ext, count in sorted_types:
        print(f"  {ext if ext else 'No Extension'}: {count}")

if __name__ == "__main__":
    scan_leftovers()
