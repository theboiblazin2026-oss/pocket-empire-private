
import os
import filecmp

def get_dir_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            try:
                total += os.path.getsize(fp)
            except: pass
    return total

def compare_folders(migrated_path, existing_path):
    print(f"Comparing:")
    print(f"  A: {migrated_path}")
    print(f"  B: {existing_path}")
    
    if not os.path.exists(migrated_path):
        print("  -> Migrated path does not exist (already cleaned?)")
        return
    if not os.path.exists(existing_path):
        print("  -> Existing path missing. Safe to move.")
        return

    size_a = get_dir_size(migrated_path)
    size_b = get_dir_size(existing_path)
    
    print(f"  Size A: {size_a:,} bytes")
    print(f"  Size B: {size_b:,} bytes")
    
    if size_a == size_b:
        print("  -> SIZES MATCH. Likely IDENTIAL.")
    else:
        diff = size_a - size_b
        print(f"  -> SIZE MISMATCH. Difference: {diff:,} bytes")
        if size_a > size_b:
            print("  -> Migrated copy is LARGER (potentially newer/more data).")
        else:
            print("  -> Existing copy is LARGER.")

def main():
    pairs = [
        ("/Volumes/CeeJay SSD/desktop_migrated/Dispatch App", "/Volumes/CeeJay SSD/Projects/Dispatch App"),
        ("/Volumes/CeeJay SSD/desktop_migrated/Jayboi_Services_Site", "/Volumes/CeeJay SSD/Projects/Jayboi_Services_Site"),
        ("/Volumes/CeeJay SSD/desktop_migrated/Infinite-Bond-Memorials", "/Volumes/CeeJay SSD/Projects/Infinite-Bond-Memorials"),
        ("/Volumes/CeeJay SSD/desktop_migrated/lead puller", "/Volumes/CeeJay SSD/Projects/lead puller"),
        ("/Volumes/CeeJay SSD/desktop_migrated/Truck Scraper Master File", "/Volumes/CeeJay SSD/Projects/Truck Scraper Master File")
    ]
    
    print("Project Collision Check")
    print("=======================")
    
    for mig, exist in pairs:
        compare_folders(mig, exist)
        print("-" * 30)

if __name__ == "__main__":
    main()
