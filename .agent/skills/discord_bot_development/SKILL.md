---
name: Discord Bot Development
description: discord.py, commands, events, and bot hosting
---

# Discord Bot Development Skill

## Basic Bot Structure

```python
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run('YOUR_TOKEN')
```

## Command Types

### Basic Command
```python
@bot.command()
async def hello(ctx, name: str):
    await ctx.send(f'Hello, {name}!')
```

### Slash Commands
```python
from discord import app_commands

@bot.tree.command(name="greet", description="Greet someone")
async def greet(interaction: discord.Interaction, name: str):
    await interaction.response.send_message(f'Hello, {name}!')
```

## Events

```python
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'hello' in message.content.lower():
        await message.channel.send('Hello!')
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    await channel.send(f'Welcome, {member.mention}!')
```

## Embeds

```python
embed = discord.Embed(
    title="Title",
    description="Description",
    color=discord.Color.blue()
)
embed.add_field(name="Field", value="Value", inline=False)
embed.set_footer(text="Footer")
await ctx.send(embed=embed)
```

## Cogs (Modular Code)

```python
# cogs/admin.py
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member):
        await member.kick()

async def setup(bot):
    await bot.add_cog(Admin(bot))
```

## Hosting Options

| Option | Cost | Uptime |
|--------|------|--------|
| Replit | Free-$7 | 24/7 (paid) |
| Railway | $5+ | 24/7 |
| VPS (DigitalOcean) | $5+ | 24/7 |
| Raspberry Pi | One-time | 24/7 (home) |

## When to Apply
Use when building Discord bots, adding commands, or debugging bot issues.
