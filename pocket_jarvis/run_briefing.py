import os
import asyncio
import discord
from dotenv import load_dotenv
from tools.briefing.generator import generate_briefing_embed

# Load Environment
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
USER_ID = int(os.getenv("DISCORD_USER_ID", "0"))

if not TOKEN or USER_ID == 0:
    print("❌ Error: Missing DISCORD_TOKEN or DISCORD_USER_ID in .env")
    exit(1)

class BriefingBot(discord.Client):
    async def on_ready(self):
        print(f'✅ Logged in as {self.user}')
        
        # Get User
        user = await self.fetch_user(USER_ID)
        if not user:
            print(f"❌ Could not find user {USER_ID}")
            await self.close()
            return

        print("generating briefing...")
        embed = generate_briefing_embed()
        
        print(f"🚀 Sending briefing to {user.name}...")
        await user.send(embed=embed)
        print("✅ Sent!")
        
        await self.close()

def main():
    intents = discord.Intents.default()
    intents.dm_messages = True
    
    bot = BriefingBot(intents=intents)
    bot.run(TOKEN)

if __name__ == "__main__":
    main()
