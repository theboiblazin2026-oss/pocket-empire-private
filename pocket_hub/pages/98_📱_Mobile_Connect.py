import streamlit as st
import subprocess
import os
import time
import signal

# Ensure local imports work
DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(DIR, '../../'))

def main():
    st.set_page_config(
        page_title="📱 Mobile Connect",
        page_icon="📱",
        layout="centered"
    )

    st.title("📱 Road Mode (Mobile Access)")
    st.caption("Securely access your dashboard from your iPad or iPhone.")

    # Status Check
    tunnel_file = os.path.join(ROOT_DIR, "mobile_url.txt")
    is_running = False
    url = None

    # Check if process is running (simple check)
    # This is a bit tricky on python without psutil, so we rely on file existence and freshness
    # or just check if pgrep finds ssh with the specific args.
    
    # Check if process is running OR if file has valid content
    try:
        # Check for ssh tunnel process
        result = subprocess.run(["pgrep", "-f", "ssh -R 80:localhost:8500"], capture_output=True)
        if result.returncode == 0:
            is_running = True
    except:
        pass
    
    # Fallback: Check if file exists and has recent content (created in last 5 mins)
    if os.path.exists(tunnel_file):
        # If file has a valid URL, assume it's running
        with open(tunnel_file, "r") as f:
            content = f.read()
            if "localhost.run" in content or "serveo.net" in content:
                is_running = True

    if is_running:
        st.success("🟢 Tunnel Active")
        
        # Read URL from file
        if os.path.exists(tunnel_file):
            with open(tunnel_file, "r") as f:
                content = f.read()
                # Debug: Print content to console if needed
                # print(content)
                
                import re
                url = None
                
                # Priority 1: Check for Cloudflare (Our new default)
                # Cloudflare outputs: https://random-string.trycloudflare.com
                if "trycloudflare.com" in content:
                     match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', content)
                     if match: 
                         url = match.group(1)
                
                # Priority 2: Check for Serveo (Backup)
                if not url and "serveo" in content:
                     # Remove ANSI escape codes
                     clean_content = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', content)
                     match = re.search(r'(https://[a-zA-Z0-9-]+\.serveo(?:usercontent)?\.(?:net|com))', clean_content)
                     if match: 
                         url = match.group(1)
                
                # Priority 3: Check for lhr.life 
                if not url:
                    match = re.search(r'(https://[a-zA-Z0-9-]+\.lhr\.life)', content)
                    if match:
                        url = match.group(1)

        if url:
            st.success(f"🔗 Connected: {url}")
            st.markdown(f"### [Click to Open on Mobile]({url})")
            st.code(url, language="text")
            
            st.info("💡 **Tip:** On your iPad, open this link in Safari, tap 'Share', and select **'Add to Home Screen'** for a full-screen app experience.")

            # Generate QR Code
            try:
                import segno
                qr = segno.make(url)
                qr_path = "mobile_qr.png"
                qr.save(qr_path, scale=10)
                st.image(qr_path, caption="Scan with Camera", width=300)
            except ImportError:
                st.warning("⚠️ QR Code generator missing. Installing...")
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "segno"], check=True)
                    st.rerun()
                except:
                     st.error("Could not auto-install 'segno'. Run `pip install segno` in terminal.")

            if st.button("🛑 Stop Tunnel"):
                subprocess.run(["pkill", "-f", "ssh -R 80:localhost:8500"])
                if os.path.exists(tunnel_file):
                    os.remove(tunnel_file)
                st.rerun()
        else:
            st.warning("Tunnel is starting... please wait a moment and refresh.")
            if st.button("🔄 Refresh"):
                st.rerun()
            
            # Show raw output for debugging
            if os.path.exists(tunnel_file):
                with open(tunnel_file, "r") as f:
                    st.text_area("Log Output", f.read(), height=100)

    else:
        st.info("🔴 Tunnel Inactive")
        st.write("Click below to generate a secure public link.")
        
        if st.button("🚀 Start Road Mode"):
            # Run the shell script
            script_path = os.path.join(ROOT_DIR, "mobile_connect.sh")
            subprocess.Popen(["/bin/bash", script_path])
            with st.spinner("Initializing secure tunnel..."):
                time.sleep(3)
            st.rerun()

    st.divider()
    st.write("### 🔒 Security Note")
    st.caption("This creates a temporary, encrypted tunnel. The link changes every time you restart it. Only share this link with yourself.")

if __name__ == "__main__":
    main()
