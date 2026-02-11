import google.generativeai as genai
import imaplib
import email
from email.header import decode_header
import streamlit as st
import os

def get_gemini_key():
    """Retrieve Gemini API Key from secrets or env"""
    if "gemini" in st.secrets and "api_key" in st.secrets["gemini"]:
        return st.secrets["gemini"]["api_key"]
    return os.environ.get("GEMINI_API_KEY")

def analyze_reply(email_body):
    """
    Analyze the sentiment and intent of a lead's reply.
    Returns a dict with sentiment, intent, and suggested_status.
    """
    api_key = get_gemini_key()
    if not api_key:
        return {"error": "No API Key"}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""
        You are a Sales Manager. Analyze this email reply from a lead.
        
        Email Body:
        "{email_body[:2000]}"
        
        Determine:
        1. Sentiment (Positive, Negative, Neutral)
        2. Intent (Interested, Not Interested, Info Needed, Unsubscribe, Out of Office)
        3. Suggested Pipeline Status (Negotiating, Lost, Contacted, No Response)
        4. Brief Summary (Max 15 words)
        
        Return ONLY valid JSON:
        {{
            "sentiment": "...",
            "intent": "...",
            "suggested_status": "...",
            "summary": "..."
        }}
        """
        
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        import json
        return json.loads(text)
        
    except Exception as e:
        return {"error": str(e)}

def fetch_latest_email(lead_email, imap_server, imap_user, imap_pass):
    """
    Fetch the text of the latest email FROM a specific address.
    """
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(imap_user, imap_pass)
        mail.select("inbox")
        
        # Search for emails FROM the lead
        status, messages = mail.search(None, f'(FROM "{lead_email}")')
        
        if status != "OK" or not messages[0]:
            return None
            
        # Get the latest one
        latest_id = messages[0].split()[-1]
        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get("Content-Disposition"))
                
                if ctype == "text/plain" and "attachment" not in cdispo:
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
            
        mail.logout()
        return body
        
    except Exception as e:
        return None
