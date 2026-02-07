import os
import shutil
import glob

home = os.path.expanduser("~")

targets = [
    # 1. Album Art (Safe to regen)
    os.path.join(home, "Library/Containers/com.apple.AMPArtworkAgent"),
    
    # 2. Specific Large Installers
    os.path.join(home, "Downloads/Antigravity.dmg"),
    os.path.join(home, "Downloads/Ollama.dmg"),
    
    # 3. Specific Caches (Don't delete the whole root folder, just contents if possible, or specific heavy ones)
    os.path.join(home, "Library/Caches/com.apple.python"),
    os.path.join(home, "Library/Caches/pip"),
    os.path.join(home, "Library/Caches/ollama"),
    os.path.join(home, "Library/Caches/com.apple.textunderstandingd"),
    
    # 4. Google Chrome Cache specifically (Protected path)
    os.path.join(home, "Library/Application Support/Google/Chrome/Default/Cache"),
    os.path.join(home, "Library/Application Support/Google/Chrome/Default/Code Cache"),
]

print("--- Starting Cleanup ---")
deleted_size = 0

def get_size(path):
    total = 0
    if os.path.isfile(path):
        return os.path.getsize(path)
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total += os.path.getsize(fp)
    return total

for target in targets:
    if os.path.exists(target):
        try:
            size = get_size(target)
            print(f"Deleting: {target} ({size / (1024*1024):.1f} MB)")
            
            if os.path.isfile(target):
                os.remove(target)
            else:
                shutil.rmtree(target)
            
            deleted_size += size
        except Exception as e:
            print(f"Error deleting {target}: {e}")
    else:
        print(f"Not found: {target}")

print(f"--- Cleanup Complete ---")
print(f"Total Reclaimed: {deleted_size / (1024*1024*1024):.2f} GB")
