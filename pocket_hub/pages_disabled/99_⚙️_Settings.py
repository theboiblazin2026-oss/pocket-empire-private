import streamlit as st
import os
import toml

def main():
    st.set_page_config(
        page_title="⚙️ Settings",
        page_icon="⚙️",
        layout="wide"
    )

    st.title("⚙️ System Settings")
    st.caption("Configure your Pocket Empire once. Run forever.")

    # --- Secrets Management ---
    st.subheader("🔑 AI Integration Keys")
    st.info("To power the **Pocket Lawyer**, **News Analyst**, and **Lead Vetta**, you need a Google Gemini API Key. It is **Free**.")
    
    st.markdown("[👉 Get your FREE Key from Google AI Studio](https://aistudio.google.com/app/apikey)")
    
    # Path to secrets
    secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    
    # Load existing
    current_key = ""
    try:
        if os.path.exists(secrets_path):
            with open(secrets_path, "r") as f:
                config = toml.load(f)
                current_key = config.get("GOOGLE_API_KEY", "")
    except Exception as e:
        st.error(f"Error loading secrets: {e}")

    # Input Form
    with st.form("api_key_form"):
        new_key = st.text_input("Google API Key", value=current_key, type="password", help="Starts with AIza...")
        
        if st.form_submit_button("💾 Save Key System-Wide"):
            try:
                # Prepare data
                data = {"GOOGLE_API_KEY": new_key}
                
                # Write to secrets.toml
                with open(secrets_path, "w") as f:
                    toml.dump(data, f)
                
                st.success("✅ Key Saved! It is now active for ALL apps (Lawyer, News, Leads).")
                st.balloons()
                
            except Exception as e:
                st.error(f"Failed to save: {e}")

    st.divider()
    
    # --- System Status ---
    st.subheader("🖥️ Launcher Status")
    st.write("Using **Pocket Empire.app** bundle.")
    if st.button("🔄 Force App Icon Refresh"):
        os.system("touch 'Pocket Empire.app' && killall Dock")
        st.success("Icon refresh command sent!")

    st.divider()
    st.caption(f"Storage Path: `{secrets_path}`")

if __name__ == "__main__":
    main()
