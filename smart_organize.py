import os
import shutil

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                try:
                    total_size += os.path.getsize(fp)
                except OSError:
                    continue
    return total_size

def scan_dir(path):
    print(f"Scanning {path}...")
    if not os.path.exists(path):
        print("Path not found.")
        return

    items = []
    try:
        for entry in os.scandir(path):
            try:
                if entry.is_dir(follow_symlinks=False):
                    size = get_size(entry.path)
                    items.append((entry.path, size))
                elif entry.is_file(follow_symlinks=False):
                    items.append((entry.path, entry.stat().st_size))
            except PermissionError:
                continue
    except PermissionError:
        print("Permission denied.")
        return

    # Sort by size (largest first)
    items.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n--- Largest Items in {path} ---")
    for path, size in items[:10]:
        print(f"{size / (1024*1024*1024):.2f} GB  {path}")

home = os.path.expanduser("~")
scan_dir(os.path.join(home, "Library/Caches"))
scan_dir(os.path.join(home, "Downloads"))

scan_dir(os.path.join(home, "Library/Application Support"))
scan_dir(os.path.join(home, "Library/Containers"))
scan_dir(os.path.join(home, "Movies"))
scan_dir(os.path.join(home, "Music"))

