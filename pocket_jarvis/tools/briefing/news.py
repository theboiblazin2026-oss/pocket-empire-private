import feedparser

def get_tech_news():
    """
    Fetches top headlines from TechCrunch or similar.
    """
    url = "http://feeds.feedburner.com/TechCrunch/"
    return _parse_feed(url, "Technoloy")

def get_logistics_news():
    """
    Fetches top headlines from FreightWaves.
    """
    url = "https://freightwaves.com/feed" 
    return _parse_feed(url, "Logistics")

def _parse_feed(url, category):
    headlines = []
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:3]:
            headlines.append(f"• [{entry.title}]({entry.link})")
    except Exception as e:
        headlines.append(f"❌ Error fetching {category}: {e}")
    
    return headlines

if __name__ == "__main__":
    print(get_tech_news())
    print(get_logistics_news())
