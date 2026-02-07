import os
import subprocess

def fast_du(path):
    print(f"--- Fast Scan: {path} ---")
    if not os.path.exists(path):
        print("Path not found.")
        return

    try:
        # du -d 1 -h | sort -h -r | head -n 10
        cmd = ["du", "-d", "1", "-h", path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        
        # Parse and sort
        items = []
        for line in lines:
            parts = line.split('\t')
            if len(parts) == 2:
                size_str, p = parts
                # Convert to bytes for sorting
                size = 0
                unit = size_str[-1].upper()
                try:
                    val = float(size_str[:-1])
                    if unit == 'G': size = val * 1024**3
                    elif unit == 'M': size = val * 1024**2
                    elif unit == 'K': size = val * 1024
                    else: size = val
                    items.append((p, size_str, size))
                except ValueError:
                    continue

        items.sort(key=lambda x: x[2], reverse=True)

        for p, size_str, size in items[:15]:
            print(f"{size_str}\t{p}")

    except Exception as e:
        print(f"Error: {e}")

home = os.path.expanduser("~")
fast_du("/Applications")
fast_du("/Users/Shared")
fast_du("/System/Library")
fast_du("/Library")
