
import shutil
import os

def copy_assets():
    # Source Paths
    logo_src = "/Volumes/CeeJay SSD/Projects/Tech Trap Solutions/app/public/assets/logo.png"
    # Flyer Source - Fallback to Truck Scraper since Tech Trap didn't have one
    flyer_src = "/Volumes/CeeJay SSD/Truck Scraper Master File/templates/flyer.png"
    
    # Dest Path
    dest_dir = "/Volumes/CeeJay SSD/Projects/lead puller/templates"
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Copy Logo
    if os.path.exists(logo_src):
        shutil.copy2(logo_src, os.path.join(dest_dir, "logo.png"))
        print(f"✅ Copied Logo from: {logo_src}")
    else:
        print(f"❌ Logo Source Not Found: {logo_src}")

    # Copy Flyer
    if os.path.exists(flyer_src):
        shutil.copy2(flyer_src, os.path.join(dest_dir, "flyer.png"))
        print(f"✅ Copied Flyer from: {flyer_src}")
    else:
        print(f"❌ Flyer Source Not Found: {flyer_src}")

if __name__ == "__main__":
    copy_assets()
