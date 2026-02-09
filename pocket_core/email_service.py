
import smtplib
import os
import mimetypes
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def get_email_credentials():
    """Retrieve email credentials from environment or known locations."""
    # Priority: Env Var > Project .env > Lead Puller .env
    password = os.getenv("GMAIL_APP_PASSWORD")
    email = os.getenv("GMAIL_USER", "Theboiblazin2026@gmail.com") # Default sender

    if not password:
        # Check standard locations
        possible_envs = [
            os.path.join(os.path.dirname(__file__), '../.env'),
            "/Volumes/CeeJay SSD/Projects/lead puller/.env", 
            "/Volumes/CeeJay SSD/Truck Scraper Master File/.env"
        ]
        
        for path in possible_envs:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        for line in f:
                            if "GMAIL_APP_PASSWORD" in line and "=" in line:
                                password = line.split("=", 1)[1].strip().strip('"').strip("'")
                                break
                except: pass
            if password: break
            
    return email, password

def send_email(to_email, subject, body, attachments=None, is_html=False):
    """
    Send an email with optional attachments.
    
    Args:
        to_email (str): Recipient email
        subject (str): Email subject
        body (str): Email body content
        attachments (list): List of tuples (filename, file_bytes) or file paths
        is_html (bool): True if body is HTML
    
    Returns:
        dict: {'success': bool, 'message': str}
    """
    sender_email, password = get_email_credentials()
    
    if not password:
        return {'success': False, 'message': "No Email Password Found. Check .env"}

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    
    msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
    
    if attachments:
        for att in attachments:
            try:
                # Check if it's a file path or bytes
                if isinstance(att, str) and os.path.exists(att):
                    with open(att, "rb") as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(att))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(att)}"'
                    msg.attach(part)
                elif isinstance(att, tuple) and len(att) == 2:
                    # (filename, bytes)
                    fname, fbytes = att
                    part = MIMEApplication(fbytes, Name=fname)
                    part['Content-Disposition'] = f'attachment; filename="{fname}"'
                    msg.attach(part)
            except Exception as e:
                print(f"Failed to attach {att}: {e}")

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        return {'success': True, 'message': "Email Sent Successfully!"}
    except Exception as e:
        return {'success': False, 'message': str(e)}

if __name__ == "__main__":
    # Test
    res = send_email("Theboiblazin2026@gmail.com", "Test from Pocket Core", "This is a test.")
    print(res)
