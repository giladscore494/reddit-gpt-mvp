import feedparser
import pandas as pd
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_forum_posts
from trend_check import check_trend_heat

def get_combined_trends(domain):
    """
    שילוב טרנדים מגוגל + חדשות + פורומים
    """
    # Google Trends
    google_trends = fetch_google_trends(domain)
    topics = google_trends["text_clean"].tolist() if not google_trends.empty else [domain]

    # Google News (RSS)
    news_feed = feedparser.parse(f"https://news.google.com/rss/search?q={domain}")
    news_titles = [entry.title for entry in news_feed.entries]

    combined_topics = set(topics + news_titles)
    data = []
    for topic in combined_topics:
        posts_df = fetch_forum_posts(topic)
        posts_count = len(posts_df)
        heat = check_trend_heat(posts_count)
        data.append({"topic": topic, "posts_count": posts_count, "heat": heat})
    return pd.DataFrame(data)
