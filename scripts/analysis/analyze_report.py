
import sys

def analyze_report(filename):
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

    internal_path = "/Users/newguy"
    external_path = "/Volumes/CeeJay SSD"

    internal_only = 0
    external_only = 0
    cross_drive = 0
    
    cross_drive_examples = []

    for group in sets:
        has_internal = any(p.startswith(internal_path) for p in group)
        has_external = any(p.startswith(external_path) for p in group)

        if has_internal and has_external:
            cross_drive += 1
            if len(cross_drive_examples) < 5:
                cross_drive_examples.append(group)
        elif has_internal:
            internal_only += 1
        elif has_external:
            external_only += 1

    print(f"Analysis of {len(sets)} duplicate sets:")
    print(f"  - Internal Only (Users/newguy): {internal_only}")
    print(f"  - External Only (CeeJay SSD): {external_only}")
    print(f"  - Cross-Drive (Both): {cross_drive}")
    
    if cross_drive > 0:
        print("\nExamples of Cross-Drive duplicates:")
        for group in cross_drive_examples:
            print("  Set:")
            for path in group:
                print(f"    {path}")

if __name__ == "__main__":
    analyze_report("duplicates_report.txt")
