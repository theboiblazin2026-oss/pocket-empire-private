import streamlit as st
import sys
import os

# --- SECURITY CHECK ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    import auth_utils
    auth_utils.require_auth()
except ImportError:
    st.error("Authentication module missing. Please contact administrator.")
    st.stop()
# ----------------------

import requests
import json
import google.generativeai as genai
from openai import OpenAI
import pypdf
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# --- RAG CONSTANTS ---
# pocket_hub/pages/ -> pocket_hub/ -> root -> pocket_lawyer/data/legal_docs
RAG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pocket_lawyer", "data", "legal_docs")
INDEX_FILE = os.path.join(RAG_DIR, "vector_index.faiss")
TEXT_STORE = os.path.join(RAG_DIR, "text_store.pkl")

# --- Page Config ---
st.set_page_config(
    page_title="Pocket Lawyer",
    page_icon="⚖️",
    layout="wide"
)

# --- RAG ENGINE ---
@st.cache_resource
def load_rag_engine():
    """Load or Build the Vector Database"""
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    if os.path.exists(INDEX_FILE) and os.path.exists(TEXT_STORE):
        index = faiss.read_index(INDEX_FILE)
        with open(TEXT_STORE, "rb") as f:
            chunks = pickle.load(f)
        return index, chunks, embedder
    
    # Build Index
    st.toast("Building Legal Knowledge Base... this runs once.")
    chunks = []
    
    # Read PDFs
    if not os.path.exists(RAG_DIR):
        try:
            os.makedirs(RAG_DIR)
        except:
             return None, None, embedder
        
    for f in os.listdir(RAG_DIR):
        if f.endswith(".pdf"):
            try:
                reader = pypdf.PdfReader(os.path.join(RAG_DIR, f))
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        # Simple chunking by page for now
                        chunks.append({"source": f, "page": i+1, "text": text})
            except:
                pass
    
    if not chunks:
        return None, None, embedder

    # Embed
    texts = [c["text"] for c in chunks]
    if not texts:
         return None, None, embedder
         
    embeddings = embedder.encode(texts)
    
    # Init FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    # Save
    faiss.write_index(index, INDEX_FILE)
    with open(TEXT_STORE, "wb") as f:
        pickle.dump(chunks, f)
        
    return index, chunks, embedder

def search_legal_docs(query, index, chunks, embedder, k=3):
    """Retrieve top k relevant chunks"""
    if not index or not chunks:
        return []
        
    q_embed = embedder.encode([query])
    D, I = index.search(np.array(q_embed).astype('float32'), k)
    
    results = []
    for idx in I[0]:
        if idx < len(chunks):
            results.append(chunks[idx])
    return results

# --- Sidebar: Settings & API Key ---
with st.sidebar:
    st.title("⚖️ Pocket Lawyer")
    st.caption("AI-Powered Legal Research")
    
    provider = st.radio("Model Provider", ["OpenAI (Cloud)", "Google Gemini (Free)"], index=1)
    
    # API Key Logic
    api_key = None
    
    # Robustly find secrets.toml
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, "../../.."))
        secrets_path = os.path.join(root_dir, ".streamlit", "secrets.toml")
        
        if not os.path.exists(secrets_path):
             secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    except:
        secrets_path = os.path.join(os.getcwd(), ".streamlit", "secrets.toml")
    
    def load_secrets_file():
        if os.path.exists(secrets_path):
            try:
                import toml
                with open(secrets_path, "r") as f:
                    return toml.load(f)
            except:
                return {}
        return {}

    if "GOOGLE_API_KEY" in st.session_state:
        api_key = st.session_state["GOOGLE_API_KEY"]
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    elif "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
        api_key = st.secrets["gemini"]["api_key"]
    
    if not api_key:
        file_secrets = load_secrets_file()
        api_key = file_secrets.get("GOOGLE_API_KEY")

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if provider == "OpenAI (Cloud)":
        user_key = st.text_input("OpenAI API Key", type="password", help="Required for GPT-4o")
        if user_key:
            api_key = user_key
        if not api_key:
             api_key = os.getenv("OPENAI_API_KEY")
             
    else: # Google Gemini
        with st.expander("🔐 API Key Settings", expanded=not api_key):
            current_val = api_key if api_key else ""
            new_key = st.text_input("Google API Key", value=current_val, type="password", help="Your auto-saved system key")
            
            if st.button("💾 Save & Lock Key"):
                try:
                    import toml
                    os.makedirs(os.path.dirname(secrets_path), exist_ok=True)
                    
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
st.caption("✅ Version 3.0 - RAG Enabled")

if "Contract" in mode:
    st.caption("Upload any contract. I'll find the risks, money traps, and extract key contacts.")
    
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
                    contract_text = ""
                    if uploaded_file.type == "application/pdf":
                        try:
                            pdf_reader = pypdf.PdfReader(uploaded_file)
                            for page in pdf_reader.pages:
                                contract_text += page.extract_text()
                        except ImportError:
                            st.error("PYPDF not installed.")
                            st.stop()
                    else:
                        contract_text = uploaded_file.getvalue().decode("utf-8")
                    
                    if provider == "Google Gemini (Free)":
                        model = genai.GenerativeModel('gemini-2.0-flash')
                        
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
    st.caption("Ask questions. Get answers backed by actual federal code.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a legal question..."):
        if not api_key:
            st.error("❌ API Key Required. Configure in sidebar.")
            st.stop()
            
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Base Prompts
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
            
            # --- RAG INJECTION ---
            try:
                index, chunks, embedder = load_rag_engine()
                if index:
                    docs = search_legal_docs(prompt, index, chunks, embedder)
                    if docs:
                        context_str = "\n\n".join([f"Source: {d['source']} (Page {d['page']})\nContent: {d['text'][:500]}..." for d in docs])
                        system_prompt += f"""
                        
                        REFERENCED LEGAL DOCUMENTS (Use these to ground your answer):
                        {context_str}
                        
                        INSTRUCTION: If the documents above serve as evidence, cite them as "According to [Source]...".
                        """
            except Exception as e:
                pass
            # ---------------------
            
            full_response = ""
            
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
                full_response = ""
                genai.configure(api_key=api_key)
                model_id = 'gemini-2.0-flash'
                
                try:
                    model = genai.GenerativeModel(model_id, system_instruction=system_prompt)
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