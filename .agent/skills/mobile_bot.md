---
name: mobile_bot
description: A skill to control your system remotely via Discord.
---

# Pocket Jarvis 📱

This skill creates a personal Discord bot that listens to your commands from your phone.

## Capabilities
1.  **Remote Control**: Run terminal commands from your phone.
2.  **Status Checks**: Ask "Is the render done?" from the road.
3.  **Two-Way Comms**: The bot can send you alerts when tasks finish.

## Setup
1.  **Create Bot**: Go to [Discord Developer Portal](https://discord.com/developers/applications).
2.  **Get Token**: Create a bot user and copy the "Token".
3.  **Install Lib**: \`pip3 install discord.py\`

## Usage

### Running the Bot
Run the script with your token:

\`\`\`bash
export DISCORD_TOKEN="your-token-here"
python3 discord_bot.py
\`\`\`

### The Code (`discord_bot.py`)
(See the accompanying python script in this folder).
It supports commands like:
- `!ping`: Health check.
- `!status`: Check if processes are running.
- `!exec <command>`: Run a terminal command (Protected by User ID).
