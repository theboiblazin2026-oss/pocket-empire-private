#!/usr/bin/env python3
"""
Reminder Check Script with Multi-Channel Notifications
Supports: Discord, macOS Native Notifications
Run this via cron hourly for timely reminders.
"""
import os
import sys
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from reminder_manager import get_due_reminders, format_reminder
import requests
from dotenv import load_dotenv

# Load environment from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'pocket_jarvis', '.env'))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")

def send_macos_notification(title, message, sound=True):
    """Send a native macOS notification popup."""
    try:
        sound_cmd = 'sound name "Glass"' if sound else ""
        script = f'''
        display notification "{message}" with title "{title}" {sound_cmd}
        '''
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"⚠️ macOS notification failed: {e}")
        return False

def send_discord_message(content):
    """Send message to Discord via webhook."""
    if DISCORD_WEBHOOK:
        try:
            requests.post(DISCORD_WEBHOOK, json={"content": content}, timeout=10)
            return True
        except Exception as e:
            print(f"⚠️ Discord send failed: {e}")
            return False
    else:
        print(content)
        return False

def main():
    now = datetime.now()
    
    # Get reminders due today and in next 3 days
    today_reminders = get_due_reminders(days_ahead=0)
    upcoming = get_due_reminders(days_ahead=3)
    
    if not today_reminders and not upcoming:
        print("No reminders due soon.")
        return
    
    # === MACOS NOTIFICATIONS (for urgent items) ===
    if today_reminders:
        for r in today_reminders:
            # Check if it's within the window for this reminder
            due_time = datetime.fromisoformat(r["due_date"])
            time_diff = (due_time - now).total_seconds()
            
            # Notify if:
            # - Overdue (negative time_diff)
            # - Due within the next hour
            # - Due exactly at this hour (for hourly cron)
            if time_diff <= 3600:  # Within 1 hour or overdue
                title = "⏰ Reminder Due!" if time_diff > 0 else "🔴 OVERDUE!"
                msg = r["title"]
                if r.get("amount"):
                    msg += f" - ${r['amount']:.2f}"
                send_macos_notification(title, msg)
    
    # === DISCORD NOTIFICATION ===
    lines = ["# 🔔 Reminder Check\\n"]
    
    if today_reminders:
        lines.append("## ⚠️ DUE TODAY / OVERDUE:")
        for r in today_reminders:
            lines.append(format_reminder(r))
        lines.append("")
    
    # Show upcoming that aren't already in today
    today_ids = {r["id"] for r in today_reminders}
    upcoming_only = [r for r in upcoming if r["id"] not in today_ids]
    
    if upcoming_only:
        lines.append("## 📅 Coming Up (Next 3 Days):")
        for r in upcoming_only:
            lines.append(format_reminder(r))
    
    message = "\\n".join(lines)
    
    # Add mention if we have user ID
    if DISCORD_USER_ID:
        message = f"<@{DISCORD_USER_ID}>\\n{message}"
    
    send_discord_message(message)
    print(f"[{now.strftime('%Y-%m-%d %H:%M')}] Checked {len(today_reminders)} due, {len(upcoming_only)} upcoming")

if __name__ == "__main__":
    main()

