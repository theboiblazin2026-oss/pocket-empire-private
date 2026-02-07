import os
import json
import discord
import asyncio
from datetime import datetime
from tools.monitor import get_carrier_status
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("DISCORD_USER_ID", "0"))

DIR = os.path.dirname(os.path.abspath(__file__))
MONITOR_FILE = os.path.join(DIR, "monitored_mcs.txt")
HISTORY_FILE = os.path.join(DIR, "history.json")

async def main():
    if not os.path.exists(MONITOR_FILE):
        print("❌ No monitored_mcs.txt found.")
        return

    # Load History
    history = {}
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                history = json.load(f)
            except:
                pass

    # Read MCs
    with open(MONITOR_FILE, 'r') as f:
        mcs = [line.strip() for line in f if line.strip()]

    if not mcs:
        print("ℹ️ No MCs to monitor.")
        return

    alerts = []
    current_state = {}

    print(f"🔍 Monitoring {len(mcs)} carriers...")

    for entry_line in mcs:
        # Handle "ID|Alias" format
        if "|" in entry_line:
            entry = entry_line.split("|")[0].strip()
        else:
            entry = entry_line
            
        # Parse TYPE:ID format (e.g., "MC:12345" or "DOT:987654")
        if ":" in entry:
            id_type, identifier = entry.split(":", 1)
            search_type = "USDOT" if id_type.upper() == "DOT" else "MC_MX"
        else:
            # Legacy format - assume MC
            identifier = entry
            search_type = "MC_MX"
            
        data = get_carrier_status(identifier, search_type=search_type)
        
        if "error" in data:
            print(f"❌ Error for {identifier}: {data['error']}")
            continue
            
        # Compare with history
        prev = history.get(identifier, {})
        
        # CHECK 1: Status Change
        if prev and prev.get('status') != data['status']:
            alerts.append(f"⚠️ **STATUS CHANGE** for `{identifier}` ({data['legal_name']})\nOld: {prev.get('status')} -> New: **{data['status']}**")
        
        # CHECK 2: Rating Change
        if prev and prev.get('rating') != data['rating']:
             alerts.append(f"🚨 **SAFETY RATING CHANGE** for `{identifier}`\nOld: {prev.get('rating')} -> New: **{data['rating']}**")

        # CHECK 3: First Run (Baseline)
        if not prev:
            alerts.append(f"🆕 **Started Monitoring** `{identifier}`\nName: {data['legal_name']}\nStatus: {data['status']}\nRating: {data['rating']}")

        current_state[identifier] = data

    # Save History
    with open(HISTORY_FILE, 'w') as f:
        json.dump(current_state, f, indent=2)

    # SEND ALERTS (One Batch)
    if alerts:
        client = discord.Client(intents=discord.Intents.default())
        
        @client.event
        async def on_ready():
            user = await client.fetch_user(USER_ID)
            if user:
                embed = discord.Embed(title="🛡️ Compliance Officer Alert", color=0xFF0000)
                desc = "\n\n".join(alerts)
                # Discord limit is 4096 chars
                if len(desc) > 4000: desc = desc[:4000] + "..."
                embed.description = desc
                try:
                    await user.send(embed=embed)
                    print("✅ Alerts sent to Discord.")
                except Exception as e:
                    print(f"❌ Failed to send Discord DM: {e}")
            await client.close()
            
        await client.start(TOKEN)

    print("✅ Monitoring Complete.")

if __name__ == "__main__":
    asyncio.run(main())
