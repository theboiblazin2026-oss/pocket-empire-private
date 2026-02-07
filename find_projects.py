
import os

def find_projects():
    targets = [
        '/Volumes/CeeJay SSD/HDD_Import_20260131',
        '/Volumes/CeeJay SSD/desktop_migrated',
        '/Volumes/CeeJay SSD/downloads_migrated'
    ]
    
    projects = []
    
    for target in targets:
        if not os.path.exists(target): continue
        
        for root, dirs, files in os.walk(target):
            if 'package.json' in files:
                # Found a Node project
                projects.append(root)
                # Don't recurse into this project's subdirs (like node_modules)
                # This keeps the list high-level
                if 'node_modules' in dirs:
                    dirs.remove('node_modules')
            
            # Optimization: Skip deep node_modules if we didn't catch it above
            if 'node_modules' in dirs:
                dirs.remove('node_modules')
            if '.git' in dirs:
                dirs.remove('.git')

    print(f"Found {len(projects)} potential Software Projects.")
    print("Top 20 Project Roots:")
    for p in projects[:30]:
        print(f"  - {p}")

if __name__ == "__main__":
    find_projects()
