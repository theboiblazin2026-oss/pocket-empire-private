import os

def inject_auth_to_pages():
    pages_dir = "/Volumes/CeeJay SSD/Projects/PocketEmpire/pocket_hub/pages"
    
    auth_block = """
# --- SECURITY CHECK ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    import streamlit as st
    st.error("Authentication module missing. Please contact administrator.")
    st.stop()
# ----------------------
"""

    for filename in os.listdir(pages_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(pages_dir, filename)
            
            with open(filepath, "r") as f:
                content = f.read()
            
            # Check if already injected
            if "import auth_utils" in content:
                print(f"Skipping {filename} - already has auth")
                continue
            
            # Insert after the first import (usually import streamlit) or at top
            lines = content.splitlines()
            new_lines = []
            inserted = False
            
            for line in lines:
                new_lines.append(line)
                # Insert after the first import statement we see
                if not inserted and (line.startswith("import ") or line.startswith("from ")):
                    new_lines.append(auth_block)
                    inserted = True
            
            # If no imports found (unlikely), prepend
            if not inserted:
                new_lines.insert(0, auth_block)
            
            with open(filepath, "w") as f:
                f.write("\n".join(new_lines))
            
            print(f"Injected auth into {filename}")

if __name__ == "__main__":
    inject_auth_to_pages()
