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
    
    api_key = None
    
    # Try loading from secrets first (System-Wide Setting)
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    
    if provider == "OpenAI (Cloud)":
        user_key = st.text_input("OpenAI API Key", type="password", help="Required for GPT-4o")
        if user_key:
            api_key = user_key
        elif not api_key:
             api_key = os.getenv("OPENAI_API_KEY")
             
    else: # Google Gemini
        # If secret is set, we don't even need to show the input box, or we can show it as "configured"
        if api_key:
            st.success("✅ System API Key Active (Gemini)")
        else:
            user_key = st.text_input("Google API Key", type="password", help="Get free at aistudio.google.com")
            if user_key:
                api_key = user_key
            elif not api_key:
                api_key = os.getenv("GOOGLE_API_KEY")
    
    st.divider()
    mode = st.radio("Practice Area", ["🚛 FMCSA / DOT (Trucking)", "💳 Consumer Credit (FCRA/FDCPA)"])
    
    st.info("⚠️ **Disclaimer:** I am an AI, not an attorney. This is for research purposes only. Consult a qualified lawyer for legal advice.")

# --- Main Interface ---
st.title(f"⚖️ {mode.split(' ')[1]} Legal Assistant")
st.caption("Ask questions. Get answers backed by actual federal code.")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("Ask a legal question (e.g., 'What are the HOS exemptions for ag haulers?')..."):
    if provider == "OpenAI (Cloud)" and not api_key:
        st.error("❌ Please enter an OpenAI API Key in the sidebar or switch to Gemini.")
        st.stop()
    if provider == "Google Gemini (Free)" and not api_key:
         st.error("❌ Please enter a Google API Key in the sidebar. Get one free at [aistudio.google.com](https://aistudio.google.com).")
         st.stop()
        
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
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
            1. CITATION REQUIRED: You MUST cite the specific US Code (e.g., "15 U.S. Code § 1681i") for every claim.
            2. BE AGGRESSIVE: Focus on consumer rights and leverage.
            3. TACTICS: Suggest specific legal disputes (e.g., "Method of Verification", "Failure to Reinvestigate").
            4. TONE: Empowering, aggressive, strategic.
            """
            
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
