import smtplib
import os
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailManager:
    def __init__(self):
        # Try to load creds from various locations
        self.username = "Theboiblazin2026@gmail.com"
        self.password = os.getenv("GMAIL_APP_PASSWORD")
        self.from_email = "Info@jayboiservicesllc.com"
        
        # If not in env, try to load from Truck Scraper .env
        if not self.password:
            try:
                env_path = "/Volumes/CeeJay SSD/Truck Scraper Master File/.env"
                if os.path.exists(env_path):
                    with open(env_path, 'r') as f:
                        for line in f:
                            if "GMAIL_APP_PASSWORD" in line:
                                self.password = line.split("=")[1].strip().strip('"').strip("'")
                                break
            except:
                pass

        if not self.password:
            logger.warning("⚠️ GMAIL_APP_PASSWORD not found. Emailing will fail.")

    def send_email(self, to_email: str, subject: str, body: str, attachments: Optional[List[str]] = None):
        """Send an email with optional attachments."""
        if not self.password:
            return {"error": "Gmail App Password not configured."}

        try:
            msg = MIMEMultipart()
            msg['From'] = f"Jayboi Services <{self.from_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'html'))

            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                        
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                        msg.attach(part)
                    else:
                        logger.warning(f"Attachment not found: {file_path}")

            # Send
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, to_email, msg.as_string())
            server.quit()
            
            return {"success": True}

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    # Test
    # m = EmailManager()
    # print(m.send_email("test@example.com", "Test", "Hello"))
    pass
