import streamlit as st
import os
from openai import OpenAI

# --- Page Config ---
st.set_page_config(
    page_title="Pocket Lawyer",
    page_icon="⚖️",
    layout="wide"
)

import requests
import json

import google.generativeai as genai

# --- Sidebar: Settings & API Key ---
with st.sidebar:
    st.title("⚖️ Pocket Lawyer")
    st.caption("AI-Powered Legal Research")
    
    provider = st.radio("Model Provider", ["OpenAI (Cloud)", "Google Gemini (Free)"], index=1)
    
    # API Key Logic
    # API Key Logic
    # Initialize with known working key (Fallback) so it works immediately
    api_key = "AIzaSyDniw4SdcQE6dZSWt7wGapY4dxu6j9SloY"
    
    # Robustly find secrets.toml
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # pages -> pocket_hub -> root (shimmering-eagle)
        root_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
        secrets_path = os.path.join(root_dir, ".streamlit", "secrets.toml")
        
        # Fallback to CWD if above fails or file missing
        if not os.path.exists(secrets_path):
             secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    except:
        secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    
    # helper to load secrets from file
    def load_secrets_file():
        if os.path.exists(secrets_path):
            try:
                import toml
                with open(secrets_path, "r") as f:
                    return toml.load(f)
            except:
                return {}
        return {}

    # 1. Try Secrets (Memory)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    # 2. Try Reading File Directly (Fallback)
    if not api_key:
        file_secrets = load_secrets_file()
        api_key = file_secrets.get("GOOGLE_API_KEY")

    # 3. Environment Variable
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    # OpenAI Logic
    if provider == "OpenAI (Cloud)":
        user_key = st.text_input("OpenAI API Key", type="password", help="Required for GPT-4o")
        if user_key:
            api_key = user_key
        if not api_key:
             api_key = os.getenv("OPENAI_API_KEY")
             
    else: # Google Gemini
        # Management UI
        with st.expander("🔐 API Key Settings", expanded=not api_key):
            current_val = api_key if api_key else ""
            new_key = st.text_input("Google API Key", value=current_val, type="password", help="Your auto-saved system key")
            
            if st.button("💾 Save & Lock Key"):
                try:
                    import toml
                    os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
                    
                    # Load existing to preserve other keys
                    file_data = load_secrets_file()
                    file_data["GOOGLE_API_KEY"] = new_key
                    
                    with open(secrets_path, "w") as f:
                        toml.dump(file_data, f)
                    
                    st.success("✅ Key Saved! Reloading...")
                    st.rerun()
                except Exception as e:
                    st.error(f"Save failed: {e}")

        if api_key:
            st.success("✅ System API Key Active")
    
    # Configure Gemini if key is available
    if api_key and provider == "Google Gemini (Free)":
        genai.configure(api_key=api_key)
    
    st.divider()
    mode = st.radio("Practice Area", [
        "🚛 FMCSA / DOT (Trucking)", 
        "💳 Consumer Credit (FCRA/FDCPA)",
        "📝 Contract Review (Universal)"
    ])
    
    st.info("⚠️ **Disclaimer:** I am an AI, not an attorney. This is for research purposes only. Consult a qualified lawyer for legal advice.")

# --- Main Interface ---
st.title(f"⚖️ {mode.split('(')[0].strip()} Assistant" if "Contract" not in mode else "⚖️ Pocket Contract Lawyer")

if "Contract" in mode:
    st.caption("Upload any contract. I'll find the risks, money traps, and extract key contacts.")
    
    # --- Contract Reader Mode ---
    
    # Context Selector
    contract_type = st.selectbox(
        "📂 What type of contract is this?",
        ["🚛 Trucking / Logistics (Broker-Carrier, Lease)", 
         "🏢 Real Estate (Lease, Purchase)", 
         "💻 Service / Freelance (SaaS, Retainer)", 
         "🤝 General Business (NDA, Partnership)", 
         "🏗️ Construction / Labor"],
    )
    
    uploaded_file = st.file_uploader("Upload Contract (PDF/TXT)", type=["pdf", "txt"])
    
    if uploaded_file and api_key:
        if st.button("🔍 Analyze Contract"):
            with st.spinner("Reading legitimate fine print..."):
                try:
                    # Text Extraction
                    contract_text = ""
                    if uploaded_file.type == "application/pdf":
                        try:
                            import pypdf
                            pdf_reader = pypdf.PdfReader(uploaded_file)
                            for page in pdf_reader.pages:
                                contract_text += page.extract_text()
                        except ImportError:
                            st.error("PYPDF not installed. Please install it or upload TXT.")
                            st.stop()
                    else:
                        # Assuming TXT
                        contract_text = uploaded_file.getvalue().decode("utf-8")
                    
                    # AI Analysis
                    if provider == "Google Gemini (Free)":
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        
                        prompt = f"""
                        You are a ruthlessly efficient contract attorney. Review this {contract_type} contract.
                        
                        Valid types of analysis for {contract_type}:
                        - Trucking: Look for Right to Offset, Pay terms, Detention, Fuel Surcharge, Cargo Claims.
                        - Real Estate: CAM charges, Subletting, Repair responsibilities, Renewal options.
                        - General/Service: IP Ownership, Non-compete, Termination for convenience, Indemnification.
                        
                        Task 1: EXTRACT CONTACTS
                        Identify all parties, names, emails, phones, and addresses mentioned.
                        
                        Task 2: RISK ANALYSIS
                        Identify the top 5 biggest risks or "gotchas". Rate the risk 1-10 (10=Bad).
                        
                        Task 3: MONEY CLAUSES
                        Summarize payment terms, penalties, and how money moves.
                        
                        CONTRACT TEXT:
                        {contract_text[:15000]}
                        """
                        
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                        
                    else:
                        st.warning("OpenAI implementation pending. Please use Gemini.")
                        
                except Exception as e:
                    st.error(f"Error analyzing contract: {e}")

else:
    # --- Chat Mode (Existing) ---
    st.caption("Ask questions. Get answers backed by actual federal code.")

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask a legal question..."):
        if not api_key:
            st.error("❌ API Key Required. Configure in sidebar.")
            st.stop()
            
        # User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # AI Response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # System Prompt Selection
            if "Trucking" in mode:
                system_prompt = """You are an expert Transportation Attorney specializing in FMCSA and DOT regulations.
                Your goal is to provide accurate, legally-backed answers to trucking questions.
                
                RULES:
                1. CITATION REQUIRED: You MUST cite the specific regulation (e.g., "49 CFR § 395.1(k)") for every claim.
                2. BE PRECISE: Distinguish between "Guidance" and "Regulation".
                3. CONTEXT: If a rule has exceptions (like Ag Exemptions, 150 air-mile radius), mention them.
                4. TONE: Professional, authoritative, but accessible.
                """
            else:
                system_prompt = """You are an expert Consumer Protection Attorney specializing in Credit Reporting (FCRA) and Debt Collection (FDCPA).
                Your goal is to help consumers repair their credit using the law.
                
                RULES:
                1. Cite § 1681 (FCRA) and § 1692 (FDCPA) sections.
                2. Be aggressive but legal.
                """
            
            try:
                if provider == "Google Gemini (Free)":
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    chat = model.start_chat(history=[])
                    response = chat.send_message(f"System: {system_prompt}\nUser: {prompt}")
                    message_placeholder.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"AI Error: {str(e)}")


            
        if provider == "OpenAI (Cloud)":
            client = OpenAI(api_key=api_key)
            try:
                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        *st.session_state.messages
                    ],
                    stream=True
                )
                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        full_response += chunk.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"OpenAI Error: {e}")

        else: # Google Gemini
            genai.configure(api_key=api_key)
            
            # Try 1.5 Flash (Latest) -> 1.5 Pro -> Pro (Old)
            model_id = 'gemini-2.5-flash'
            
            try:
                model = genai.GenerativeModel(model_id, system_instruction=system_prompt)
                # Convert session state messages to Gemini format (history)
                history = []
                for m in st.session_state.messages[:-1]: 
                    role = "user" if m["role"] == "user" else "model"
                    history.append({"role": role, "parts": [m["content"]]})
                
                chat = model.start_chat(history=history)
                response = chat.send_message(prompt, stream=True)
                for chunk in response:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
            except Exception as e:
                st.error(f"Gemini Error ({model_id}): {e}")
                st.info("💡 Troubleshooting: Check your API Key or try a different model in settings.")
                st.code("Available Models: " + str([m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]))
