import streamlit as st
import sys
import os
from datetime import datetime

# Ensure local imports
DIR = os.path.dirname(os.path.abspath(__file__))
if DIR not in sys.path:
    sys.path.insert(0, DIR)

from news_manager import (
    load_data, fetch_all_feeds, get_articles, get_feeds, 
    add_feed, remove_feed, generate_daily_briefing, last_fetch_time
)

def main():
    try:
        st.set_page_config(
            page_title="📰 News Curator",
            page_icon="📰",
            layout="wide"
        )
    except:
        pass

    st.title("📰 News Curator")
    st.caption("Aggregated trucking industry news in one place")

    # Refresh button in sidebar
    with st.sidebar:
        st.subheader("⚙️ Controls")
        
        if st.button("🔄 Refresh News", use_container_width=True):
            with st.spinner("Fetching latest news..."):
                articles = fetch_all_feeds()
                st.success(f"✅ Fetched {len(articles)} articles!")
                st.rerun()
        
        last = last_fetch_time()
        if last:
            st.caption(f"Last updated: {datetime.fromisoformat(last).strftime('%b %d, %I:%M %p')}")
        else:
            st.warning("News not fetched yet. Click 'Refresh News'.")
        
        st.divider()
        
        # Category filter
        st.subheader("📂 Filter")
        categories = ["All", "trucking", "general"]
        selected_cat = st.selectbox("Category", categories)
        
        st.divider()
        
        # Feed management
        st.subheader("📡 Feeds")
        feeds = get_feeds()
        st.caption(f"{len(feeds)} feeds configured")
        
        for feed in feeds:
            st.caption(f"• {feed['name']}")

    # Main content
    tab1, tab2, tab3 = st.tabs(["📰 News Feed", "📋 Daily Briefing", "⚙️ Manage Feeds"])

    with tab1:
        st.subheader("📰 Latest News")
        
        # Get articles
        cat_filter = None if selected_cat == "All" else selected_cat
        articles = get_articles(category=cat_filter, limit=30)
        
        if not articles:
            st.info("🔄 No articles yet. Click 'Refresh News' in the sidebar to fetch the latest.")
        else:
            for article in articles:
                # Parse date
                try:
                    pub_date = datetime.fromisoformat(article["published"])
                    date_str = pub_date.strftime("%b %d, %I:%M %p")
                except:
                    date_str = "Unknown date"
                
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        st.markdown(f"### [{article['title']}]({article['link']})")
                        st.caption(f"📌 {article['source']} • {date_str}")
                        
                        if article.get('summary'):
                            st.write(article['summary'][:200] + "..." if len(article.get('summary', '')) > 200 else article['summary'])
                    
                    with col2:
                        st.markdown(f"[Read →]({article['link']})")
                    
                    st.divider()

    with tab2:
        st.subheader("📋 Daily Briefing")
        
        if st.button("📝 Generate Briefing"):
            with st.spinner("Generating briefing..."):
                briefing = generate_daily_briefing()
                st.markdown(briefing)
        else:
            # Show existing briefing
            articles = get_articles(limit=15)
            if articles:
                st.markdown(f"### 📰 Top Stories - {datetime.now().strftime('%B %d, %Y')}")
                
                for i, article in enumerate(articles[:10], 1):
                    st.markdown(f"**{i}. [{article['title']}]({article['link']})**")
                    st.caption(f"Source: {article['source']}")
                    
                    if i <= 3 and article.get('summary'):
                        st.write(article['summary'][:150] + "...")
                    
                    st.divider()
            else:
                st.info("Refresh news to generate your daily briefing.")

    with tab3:
        st.subheader("⚙️ Manage RSS Feeds")
        
        # Add new feed
        with st.form("add_feed"):
            st.write("**Add New Feed**")
            col1, col2 = st.columns(2)
            
            with col1:
                feed_name = st.text_input("Feed Name", placeholder="e.g., FreightWaves")
                feed_url = st.text_input("RSS URL", placeholder="https://example.com/feed")
            
            with col2:
                feed_category = st.selectbox("Category", ["trucking", "general", "business", "tech"])
            
            if st.form_submit_button("➕ Add Feed"):
                if feed_name and feed_url:
                    result = add_feed(feed_name, feed_url, feed_category)
                    if result:
                        st.success(f"✅ Added: {feed_name}")
                        st.rerun()
                    else:
                        st.warning("Feed URL already exists.")
                else:
                    st.error("Please fill in all fields.")
        
        st.divider()
        
        # Current feeds
        st.write("**Current Feeds:**")
        feeds = get_feeds()
        
        if feeds:
            for feed in feeds:
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"📡 **{feed['name']}**")
                with col2:
                    st.caption(feed['url'][:50] + "..." if len(feed['url']) > 50 else feed['url'])
                with col3:
                    if st.button("🗑️", key=f"del_{feed['url']}"):
                        remove_feed(feed['url'])
                        st.rerun()
        else:
            st.info("No feeds configured.")

    # Footer
    st.divider()
    st.caption("💡 Tip: Add RSS feeds from your favorite trucking news sites!")

if __name__ == "__main__":
    main()
