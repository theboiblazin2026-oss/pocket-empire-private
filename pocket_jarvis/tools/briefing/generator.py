import discord
from datetime import datetime
from .weather import get_weather
from .finance import get_finance_brief
from .news import get_tech_news, get_logistics_news
from .system import get_system_health
from .agents import get_agent_stats

def generate_briefing_embed():
    """
    Gathers all data and returns a Discord Embed object (or dict).
    """
    # 1. Gather Data
    weather = get_weather()
    finance = get_finance_brief()
    sys_health = get_system_health()
    agent_stats = get_agent_stats()
    
    tech_news = get_tech_news()
    logistics_news = get_logistics_news()

    # 2. Build Embed
    title = f"🌅 Morning Briefing: {datetime.now().strftime('%A, %B %d')}"
    desc = f"Good morning, Sir. Here is your daily status report."
    
    embed = discord.Embed(title=title, description=desc, color=0x00ff00)
    
    # Weather
    w_str = f"**{weather.get('condition', 'Unknown')}** • {weather.get('temp_now', 'N/A')}°F\nH: {weather.get('high')}°F • L: {weather.get('low')}°F"
    embed.add_field(name="🌤️ Weather (Atlanta)", value=w_str, inline=True)
    
    # Finance
    f_str = f"S&P 500: {finance.get('sp500')}\nBTC: {finance.get('btc')}\n**Goal**: {finance.get('budget_goal')}"
    embed.add_field(name="💰 Market & Budget", value=f_str, inline=True)
    
    # System Health (WiFi/BT Special Request)
    s_str = f"CPU: {sys_health.get('cpu_percent')}% • RAM: {sys_health.get('ram_percent')}%\n"
    s_str += f"Validating Connections...\n"
    s_str += f"📡 WiFi: **{sys_health.get('wifi_status')}**\n"
    s_str += f"🦷 Bluetooth: **{sys_health.get('bt_status')}**"
    embed.add_field(name="🖥️ System Status", value=s_str, inline=False)

    # Agent Report Card
    a_str = f"**Lead Enricher**: {agent_stats.get('enricher_status')}\nEmails Sent: `{agent_stats.get('enricher_emails')}`\n"
    a_str += f"**Lead Puller**: {agent_stats.get('lead_puller_status')}\nLeads Found: `{agent_stats.get('lead_puller_leads')}`"
    embed.add_field(name="🤖 Agent Report Card", value=a_str, inline=False)
    
    # News
    embed.add_field(name="🚚 Logistics News", value="\n".join(logistics_news), inline=False)
    embed.add_field(name="📱 Tech News", value="\n".join(tech_news), inline=False)

    embed.set_footer(text="Pocket Jarvis V1 • System Online")
    
    return embed
