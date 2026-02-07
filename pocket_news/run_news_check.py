import sys
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))
from news_manager import fetch_all_feeds, generate_daily_briefing

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_webhook(content):
    if not WEBHOOK_URL:
        print("❌ No Discord Webhook URL found in .env")
        return False
    
    data = {
        "content": content,
        "username": "Zero Link Logistics News",
        "avatar_url": "https://cdn-icons-png.flaticon.com/512/2965/2965879.png" # Simple newspaper icon
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()
        print("✅ Sent to Discord")
        return True
    except Exception as e:
        print(f"❌ Error sending to Discord: {e}")
        return False

def main():
    print(f"[{datetime.now()}] running news check...")
    
    # 1. Fetch new articles
    articles = fetch_all_feeds()
    print(f"Fetched {len(articles)} articles.")
    
    # 2. Generate Briefing
    briefing = generate_daily_briefing()
    
    # 3. Add header based on time of day
    hour = datetime.now().hour
    if hour < 12:
        greeting = "☕ **Morning Briefing**"
    elif hour < 17:
        greeting = "☀️ **Mid-Day Update**"
    elif hour < 21:
        greeting = "🌇 **Evening Wrap-up**"
    else:
        greeting = "🌙 **Nightly News**"
        
    full_message = f"{greeting}\n\n{briefing}\n\n*Check the full dashboard for more: http://localhost:8505*"
    
    # 4. Limit length (Discord limit 2000 chars)
    if len(full_message) > 1900:
        full_message = full_message[:1900] + "...\n(Truncated)"
        
    # 5. Send
    send_discord_webhook(full_message)

if __name__ == "__main__":
    main()
