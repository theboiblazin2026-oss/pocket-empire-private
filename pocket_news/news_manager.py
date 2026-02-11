import json
import os
from datetime import datetime, timedelta
import feedparser
import requests
from bs4 import BeautifulSoup
import re

DATA_FILE = os.path.join(os.path.dirname(__file__), "feeds.json")

def load_data():
    """Load feed data from JSON."""
    if not os.path.exists(DATA_FILE):
        return {
            "feeds": [],
            "articles": [],
            "last_fetch": None
        }
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    """Save feed data to JSON."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def add_feed(name, url, category="general"):
    """Add a new RSS feed."""
    data = load_data()
    
    # Check for duplicates
    for feed in data["feeds"]:
        if feed["url"] == url:
            return None  # Already exists
    
    data["feeds"].append({
        "name": name,
        "url": url,
        "category": category
    })
    save_data(data)
    return True

def remove_feed(url):
    """Remove a feed by URL."""
    data = load_data()
    data["feeds"] = [f for f in data["feeds"] if f["url"] != url]
    save_data(data)

def get_feeds():
    """Get all configured feeds."""
    return load_data().get("feeds", [])

def fetch_feed(feed_url, feed_name):
    """Fetch articles from a single feed."""
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        
        for entry in feed.entries[:10]:  # Limit to 10 per feed
            # Parse date
            pub_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                pub_date = datetime(*entry.published_parsed[:6]).isoformat()
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                pub_date = datetime(*entry.updated_parsed[:6]).isoformat()
            else:
                pub_date = datetime.now().isoformat()
            
            # Clean summary
            summary = ""
            if hasattr(entry, 'summary'):
                soup = BeautifulSoup(entry.summary, 'html.parser')
                summary = soup.get_text()[:300]
            
            articles.append({
                "title": entry.title if hasattr(entry, 'title') else "No Title",
                "link": entry.link if hasattr(entry, 'link') else "",
                "summary": summary,
                "source": feed_name,
                "published": pub_date,
                "fetched_at": datetime.now().isoformat()
            })
        
        return articles
    except Exception as e:
        print(f"Error fetching {feed_url}: {e}")
        return []

def fetch_all_feeds():
    """Fetch all configured feeds and store articles."""
    data = load_data()
    all_articles = []
    
    for feed in data["feeds"]:
        articles = fetch_feed(feed["url"], feed["name"])
        for a in articles:
            a["category"] = feed.get("category", "general")
        all_articles.extend(articles)
    
    # Sort by published date (newest first)
    all_articles.sort(key=lambda x: x.get("published", ""), reverse=True)
    
    # Keep only last 100 articles
    data["articles"] = all_articles[:100]
    data["last_fetch"] = datetime.now().isoformat()
    save_data(data)
    
    return all_articles

def get_articles(category=None, limit=20):
    """Get stored articles, optionally filtered by category."""
    data = load_data()
    articles = data.get("articles", [])
    
    if category:
        articles = [a for a in articles if a.get("category") == category]
    
    return articles[:limit]

def get_today_articles():
    """Get articles from today."""
    today = datetime.now().date()
    articles = get_articles(limit=100)
    
    today_articles = []
    for a in articles:
        try:
            pub_date = datetime.fromisoformat(a["published"]).date()
            if pub_date == today:
                today_articles.append(a)
        except:
            pass
    
    return today_articles

def generate_daily_briefing():
    """Generate a daily news briefing summary."""
    articles = get_today_articles()
    
    if not articles:
        articles = get_articles(limit=10)
    
    briefing = f"📰 **Daily News Briefing** - {datetime.now().strftime('%B %d, %Y')}\n\n"
    
    # Group by source
    by_source = {}
    for a in articles[:15]:
        source = a.get("source", "Unknown")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(a)
    
    # Gemini Summarization
    try:
        import sys
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from pocket_core.ai_helper import ask_gemini

        news_text = "Summarize these headlines into a 5-bullet executive briefing for a trucking business owner (focus on rates, fuel, regulations, and market trends):\n\n"
        for a in articles[:20]:
            news_text += f"- {a.get('title', 'No Title')} ({a.get('source', '')})\n"
        
        text, error = ask_gemini(news_text)
        if text:
            briefing += text
            briefing += "\n\n*(Analysis by Google Gemini)*"
        else:
            # Fallback — no key or AI error
            briefing += f"**(AI Summarization Unavailable)** {error or ''}\n\n"
            for source, arts in by_source.items():
                briefing += f"**{source}:**\n"
                for a in arts[:3]:
                    briefing += f"• {a['title']}\n"
                briefing += "\n"
                
    except Exception as e:
        briefing += f"⚠️ **AI Error:** {e}\n\n"
        for source, arts in by_source.items():
            briefing += f"**{source}:**\n"
            for a in arts[:3]:
                briefing += f"• {a['title']}\n"
            briefing += "\n"
    
    return briefing

def last_fetch_time():
    """Get the last fetch timestamp."""
    data = load_data()
    return data.get("last_fetch")
