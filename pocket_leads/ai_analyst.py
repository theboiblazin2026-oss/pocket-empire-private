import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pocket_core.ai_helper import ask_gemini, parse_json_response

import imaplib
import email
from email.header import decode_header
import streamlit as st

def analyze_reply(email_body):
    """
    Analyze the sentiment and intent of a lead's reply.
    Returns a dict with sentiment, intent, and suggested_status.
    """
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
    
    text, error = ask_gemini(prompt)
    if error:
        return {"error": error}
    
    parsed, parse_error = parse_json_response(text)
    if parse_error:
        return {"error": parse_error}
    
    return parsed

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
