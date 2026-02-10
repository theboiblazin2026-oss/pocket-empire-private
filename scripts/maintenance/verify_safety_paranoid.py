
import os

def is_discard_zone(path):
    # Only files in these specific "import" type folders are candidates for deletion
    discard_markers = [
        '/HDD_Import',
        '/desktop_migrated',
        '/downloads_migrated',
        '/library_caches_migrated'
    ]
    return any(marker in path for marker in discard_markers)

def is_protected_zone(path):
    # Files here act as the "Safety Net"
    # We essentially trust that if it's in Documents/Projects, it's the "Real" one.
    protected_markers = [
        '/Volumes/CeeJay SSD/Documents',
        '/Volumes/CeeJay SSD/Projects',
        '/Volumes/CeeJay SSD/Movies',
        '/Volumes/CeeJay SSD/Music',
        '/Volumes/CeeJay SSD/Pictures',
        '/Volumes/CeeJay SSD/Ollama_Models',
        '/Volumes/CeeJay SSD/Local_Models',
        '/Users/newguy/Documents',
        '/Users/newguy/Projects'
    ]
    return any(marker in path for marker in protected_markers)

def is_sensitive_content(path):
    # KEY SAFETY CHECK: Explicitly prevent deletion of Agentic/Brain/System files
    sensitive_keywords = [
        '.gemini',
        'antigravity',
        'brain',
        'memory',
        'Jarvis',
        'super_computer',
        '.git',
        'node_modules',
        '.app',
        '.Trash',
        'System Volume Information'
    ]
    return any(keyword in path for keyword in sensitive_keywords)

def verify_safety_paranoid(filename):
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

    safe_deletions = [] # Tuple of (deletion_path, safety_net_path)
    skipped_sensitive = 0
    skipped_no_safety_net = 0
    
    total_reclaimable_size = 0

    for group in sets:
        path = group[0]
        try:
            size_per_file = os.path.getsize(path)
        except:
            size_per_file = 0

        # 1. Identify valid Safety Nets in this group
        safety_nets = [p for p in group if is_protected_zone(p) and not is_sensitive_content(p)]
        
        # 2. Identify Candidates for deletion
        # Must be in Discard Zone AND NOT Sensitive
        candidates = [p for p in group if is_discard_zone(p) and not is_sensitive_content(p)]

        if safety_nets and candidates:
            # We have at least one Safety Net. All candidates are safe to delete.
            # We pick the first safety net as the "Proof" for the manifest.
            proof = safety_nets[0]
            
            for candidate in candidates:
                # Double check they aren't the same file (impossible by def, but paranoid check)
                if candidate != proof:
                    safe_deletions.append((candidate, proof, size_per_file))
                    total_reclaimable_size += size_per_file
        
        else:
            # Check why we failed
            if any(is_sensitive_content(p) for p in group):
                skipped_sensitive += 1
            else:
                skipped_no_safety_net += 1

    # Write Manifest
    manifest_path = "deletion_manifest.txt"
    with open(manifest_path, 'w') as f:
        f.write("DELETION MANIFEST - VERIFICATION LOG\n")
        f.write("====================================\n")
        f.write(f"This file lists every file proposed for deletion.\n")
        f.write(f"Format: [DELETE] <candidate>  <-- SECURED BY --> [KEEP] <proof>\n\n")
        
        for cand, proof, size in safe_deletions:
            f.write(f"[DELETE] {cand}\n")
            f.write(f"    --> SECURED BY: {proof}\n")
            f.write("-" * 80 + "\n")

    print(f"Paranoid Verification Complete.")
    print(f"Manifest written to: {manifest_path}")
    print("-" * 30)
    print(f"Total Safe Deletions: {len(safe_deletions)}")
    print(f"Total Reclaimable Space: {total_reclaimable_size / (1024*1024*1024):.2f} GB")
    print("-" * 30)
    print(f"Sets Skipped (Sensitive Content): {skipped_sensitive}")
    print(f"Sets Skipped (No Clear Safety Net): {skipped_no_safety_net}")

if __name__ == "__main__":
    verify_safety_paranoid("duplicates_report.txt")
