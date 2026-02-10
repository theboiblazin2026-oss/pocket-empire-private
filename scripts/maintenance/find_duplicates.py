import os
import hashlib
from collections import defaultdict

def get_file_hash(filepath, partial=False):
    """Calculates SHA256 hash of a file. If partial is True, only reads first 4KB."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            if partial:
                buf = f.read(4096)
                hasher.update(buf)
            else:
                while True:
                    buf = f.read(65536)
                    if not buf:
                        break
                    hasher.update(buf)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None

def find_duplicates(folders):
    # Files grouped by size
    size_map = defaultdict(list)
    
    # Exclusions
    exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'Library', '.Trash', '.gemini'}
    exclude_files = {'.DS_Store'}

    print("Scanning directories...")
    file_count = 0
    
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            
            for filename in files:
                if filename in exclude_files or filename.startswith('.'):
                    continue
                
                filepath = os.path.join(root, filename)
                try:
                    # filtering out symbolic links
                    if os.path.islink(filepath):
                        continue
                        
                    size = os.path.getsize(filepath)
                    # Ignore empty files or very small files (< 1 byte)
                    if size > 0:
                        size_map[size].append(filepath)
                        file_count += 1
                        if file_count % 1000 == 0:
                            print(f"Scanned {file_count} files...", end='\r')
                except (PermissionError, OSError):
                    continue

    print(f"\nFinished scanning {file_count} files.")
    print("Analyzing potential duplicates by size...")

    # Filter out sizes with only 1 file
    potential_duplicates = {size: paths for size, paths in size_map.items() if len(paths) > 1}
    
    # Check partial hashes
    print("Checking partial hashes...")
    full_hash_candidates = defaultdict(list)
    
    for size, paths in potential_duplicates.items():
        partial_hashes = defaultdict(list)
        for path in paths:
            phash = get_file_hash(path, partial=True)
            if phash:
                partial_hashes[phash].append(path)
        
        for phash, p_paths in partial_hashes.items():
            if len(p_paths) > 1:
                # If partial hashes match, we need to check full hash
                for path in p_paths:
                    full_hash_candidates[(size, phash)].append(path)

    # Check full hashes
    print("Checking full hashes for confirmed duplicates...")
    final_duplicates = []
    
    for (size, phash), paths in full_hash_candidates.items():
        full_hashes = defaultdict(list)
        for path in paths:
            fhash = get_file_hash(path, partial=False)
            if fhash:
                full_hashes[fhash].append(path)
        
        for fhash, f_paths in full_hashes.items():
            if len(f_paths) > 1:
                final_duplicates.append(f_paths)

    return final_duplicates

if __name__ == "__main__":
    # Define paths to scan
    # Note: Using expanduser to handle absolute paths correctly if needed, 
    # but the paths here are passed directly.
    scan_paths = [
        '/Volumes/CeeJay SSD',
        '/Users/newguy'
    ]
    
    # Validate paths exist
    valid_paths = [p for p in scan_paths if os.path.exists(p)]
    
    if not valid_paths:
        print("No valid paths found to scan.")
    else:
        print(f"Starting scan on: {', '.join(valid_paths)}")
        duplicates = find_duplicates(valid_paths)
        
        if duplicates:
            print("\n" + "="*50)
            print(f"FOUND {len(duplicates)} SETS OF DUPLICATE FILES")
            print("="*50 + "\n")
            
            total_wasted = 0
            
            for i, group in enumerate(duplicates, 1):
                size = os.path.getsize(group[0])
                total_wasted += size * (len(group) - 1)
                
                print(f"Set {i} (Size: {size:,} bytes):")
                for path in group:
                    print(f"  - {path}")
                print("-" * 30)
            
            print(f"\nTotal potentially recoverable space: {total_wasted / (1024*1024):.2f} MB")
        else:
            print("\nNo duplicates found.")
