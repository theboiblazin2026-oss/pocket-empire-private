
import os
import sys

def execute_deletion(manifest_path, log_path):
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest file {manifest_path} not found.")
        return

    print(f"Reading manifest: {manifest_path}")
    
    with open(manifest_path, 'r') as f:
        lines = f.readlines()

    deletion_targets = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("[DELETE]"):
            # Format: [DELETE] /path/to/file
            target = line[9:].strip() 
            deletion_targets.append(target)

    print(f"Found {len(deletion_targets)} files marked for deletion.")
    
    deleted_count = 0
    reclaimed_bytes = 0
    errors = 0
    
    with open(log_path, 'w') as log:
        log.write("DELETION LOG\n")
        log.write("============\n")
        
        for target in deletion_targets:
            try:
                if os.path.exists(target):
                    size = os.path.getsize(target)
                    os.remove(target)
                    deleted_count += 1
                    reclaimed_bytes += size
                    log.write(f"[Deleted] {target} ({size} bytes)\n")
                    
                    if deleted_count % 100 == 0:
                        print(f"Deleted {deleted_count} files...", end='\r')
                else:
                    log.write(f"[Missing] {target} - file already gone\n")
            except OSError as e:
                errors += 1
                log.write(f"[Error] Failed to delete {target}: {e}\n")

    print(f"\nDeletion Complete.")
    print(f"Total Deleted: {deleted_count}")
    print(f"Total Reclaimed: {reclaimed_bytes / (1024*1024*1024):.2f} GB")
    print(f"Errors: {errors}")
    print(f"Log written to: {log_path}")

if __name__ == "__main__":
    execute_deletion("deletion_manifest.txt", "deletion_log.txt")
