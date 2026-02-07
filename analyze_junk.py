import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def get_size(start_path):
    total_size = 0
    file_count = 0
    try:
        if os.path.isfile(start_path):
            return os.path.getsize(start_path), 1
        
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    try:
                        total_size += os.path.getsize(fp)
                        file_count += 1
                    except OSError:
                        pass
    except Exception as e:
        pass
    return total_size, file_count

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def scan_junk():
    home = str(Path.home())
    
    # Categories to scan
    scan_targets = {
        "User Caches": os.path.join(home, "Library/Caches"),
        "User Logs": os.path.join(home, "Library/Logs"),
        "Xcode DerivedData": os.path.join(home, "Library/Developer/Xcode/DerivedData"),
        "Android Studio Builds": os.path.join(home, "Library/Caches/Google/AndroidStudio*"),
        "Trash": os.path.join(home, ".Trash"),
        "Downloads (Old)": os.path.join(home, "Downloads") # Logic needed for "old"
    }

    print("==========================================")
    print("      SYSTEM JUNK ANALYSIS REPORT       ")
    print("==========================================")
    
    total_junk_size = 0
    
    for category, path in scan_targets.items():
        if "*" in path:
            # Handle glob patterns if needed, but for now specific paths
            continue
            
        if not os.path.exists(path):
            continue
            
        size_bytes, count = get_size(path)
        
        # Special logic for Downloads (only count files > 30 days)
        if category == "Downloads (Old)":
            size_bytes = 0
            count = 0
            cutoff = datetime.now() - timedelta(days=30)
            try:
                for f in os.listdir(path):
                    fp = os.path.join(path, f)
                    if os.path.isfile(fp):
                        mtime = datetime.fromtimestamp(os.path.getmtime(fp))
                        if mtime < cutoff:
                            size_bytes += os.path.getsize(fp)
                            count += 1
            except:
                pass

        total_junk_size += size_bytes
        print(f"[{category}]")
        print(f"  Path: {path}")
        print(f"  Size: {format_size(size_bytes)}")
        print(f"  Files: {count}")
        print("------------------------------------------")

    print(f"\nTOTAL 'POTENTIAL JUNK' FOUND: {format_size(total_junk_size)}")
    print("==========================================")
    print("Note: 'User Caches' regenerate and speed up apps.")
    print("Deleting them clears space but may slow down app launch once.")

if __name__ == "__main__":
    scan_junk()
