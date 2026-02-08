import streamlit as st
import os
import toml

# Theme configurations
THEMES = {
    "Dark Gold (Default)": {
        "primaryColor": "#FFD700",
        "backgroundColor": "#0E1117",
        "secondaryBackgroundColor": "#262730",
        "textColor": "#FAFAFA"
    },
    "Light Mode": {
        "primaryColor": "#1E88E5",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730"
    },
    "Dark Blue": {
        "primaryColor": "#00D4FF",
        "backgroundColor": "#0D1B2A",
        "secondaryBackgroundColor": "#1B263B",
        "textColor": "#E0E1DD"
    },
    "Dark Green": {
        "primaryColor": "#00FF88",
        "backgroundColor": "#0B1A0B",
        "secondaryBackgroundColor": "#1A2F1A",
        "textColor": "#E8F5E9"
    }
}

def get_config_path():
    # Check for .streamlit in project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return os.path.join(project_root, ".streamlit", "config.toml")

def load_current_theme():
    config_path = get_config_path()
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = toml.load(f)
                theme = config.get('theme', {})
                bg = theme.get('backgroundColor', '#0E1117')
                
                # Match to theme name
                for name, colors in THEMES.items():
                    if colors['backgroundColor'] == bg:
                        return name
        return "Dark Gold (Default)"
    except:
        return "Dark Gold (Default)"

def save_theme(theme_name):
    config_path = get_config_path()
    theme = THEMES.get(theme_name, THEMES["Dark Gold (Default)"])
    
    config = {
        "theme": {
            "primaryColor": theme["primaryColor"],
            "backgroundColor": theme["backgroundColor"],
            "secondaryBackgroundColor": theme["secondaryBackgroundColor"],
            "textColor": theme["textColor"],
            "font": "sans serif"
        },
        "browser": {
            "gatherUsageStats": False
        }
    }
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            toml.dump(config, f)
        return True
    except Exception as e:
        st.error(f"Failed to save theme: {e}")
        return False

def main():
    try:
        st.set_page_config(
            page_title="⚙️ Settings",
            page_icon="⚙️",
            layout="wide"
        )
    except:
        pass

    st.title("⚙️ System Settings")
    st.caption("Configure your Pocket Empire once. Run forever.")

    # --- Theme Selector ---
    st.subheader("🎨 App Theme")
    
    current_theme = load_current_theme()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_theme = st.selectbox(
            "Choose Theme",
            list(THEMES.keys()),
            index=list(THEMES.keys()).index(current_theme)
        )
        
        # Preview colors
        theme_colors = THEMES[selected_theme]
        st.markdown(f"""
        <div style="display: flex; gap: 10px; margin-top: 10px;">
            <div style="width: 50px; height: 50px; background-color: {theme_colors['primaryColor']}; border-radius: 8px;" title="Accent"></div>
            <div style="width: 50px; height: 50px; background-color: {theme_colors['backgroundColor']}; border-radius: 8px; border: 1px solid #666;" title="Background"></div>
            <div style="width: 50px; height: 50px; background-color: {theme_colors['secondaryBackgroundColor']}; border-radius: 8px; border: 1px solid #666;" title="Sidebar"></div>
            <div style="width: 50px; height: 50px; background-color: {theme_colors['textColor']}; border-radius: 8px;" title="Text"></div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("💾 Apply Theme", use_container_width=True):
            if save_theme(selected_theme):
                st.success(f"Theme saved! **Refresh the page** to see changes.")
                st.balloons()
    
    st.info("💡 After applying, **refresh the browser** (Ctrl+R or Cmd+R) to see the new theme.")
    
    st.divider()

    # --- Secrets Management ---
    st.subheader("🔑 AI Integration Keys")
    st.info("To power the **Pocket Lawyer**, **News Analyst**, and **Lead Vetta**, you need a Google Gemini API Key. It is **Free**.")
    
    st.markdown("[👉 Get your FREE Key from Google AI Studio](https://aistudio.google.com/app/apikey)")
    
    # Path to secrets
    # Use absolute path relative to this file to be robust
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    secrets_path = os.path.join(project_root, ".streamlit", "secrets.toml")
    
    # Load existing
    current_key = ""
    supabase_url = ""
    supabase_key = ""
    try:
        if os.path.exists(secrets_path):
            with open(secrets_path, "r") as f:
                config = toml.load(f)
                current_key = config.get("GOOGLE_API_KEY", "")
                supabase_url = config.get("SUPABASE_URL", "")
                supabase_key = config.get("SUPABASE_KEY", "")
    except Exception as e:
        st.error(f"Error loading secrets: {e}")

    # Input Form
    with st.form("api_key_form"):
        new_key = st.text_input("Google API Key", value=current_key, type="password", help="Starts with AIza...")
        new_supa_url = st.text_input("Supabase URL", value=supabase_url, help="Your project URL")
        new_supa_key = st.text_input("Supabase Key", value=supabase_key, type="password", help="Your anon/public key")
        
        if st.form_submit_button("💾 Save Keys"):
            try:
                # Prepare data
                data = {
                    "GOOGLE_API_KEY": new_key,
                    "SUPABASE_URL": new_supa_url,
                    "SUPABASE_KEY": new_supa_key
                }
                
                # Write to secrets.toml
                os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
                with open(secrets_path, "w") as f:
                    toml.dump(data, f)
                
                st.success("✅ Keys Saved! Streamlit will now reload.")
                st.balloons()
                
            except Exception as e:
                st.error(f"Failed to save: {e}")

    st.divider()
    
    # --- System Status ---
    st.subheader("🖥️ System Info")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Platform", "Streamlit Cloud" if os.getenv("STREAMLIT_SHARING") else "Local")
    with c2:
        st.metric("Theme", current_theme.split(" ")[0])
    with c3:
        st.metric("Version", "v1.0")
    
    st.divider()
    st.caption(f"Config Path: `{get_config_path()}`")

if __name__ == "__main__":
    main()

