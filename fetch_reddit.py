import datetime
import pandas as pd
import streamlit as st

# מנסה לייבא את PRAW רק אם יש מפתחות Reddit
try:
    import praw
    USE_REDDIT_API = True
except ImportError:
    USE_REDDIT_API = False

from fetch_websearch import fetch_websearch

def fetch_reddit_posts(keywords, days=7, limit=50):
    """
    מחזיר פוסטים רלוונטיים מ-Reddit לפי מילות מפתח.
    אם יש מפתחות Reddit → משתמש ב-API.
    אחרת → עושה חיפוש גוגל (Fallback).
    """
    posts = []
    end_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)

    # מצב 1: שימוש ב-Reddit API (אם קיימים מפתחות)
    if USE_REDDIT_API and "reddit" in st.secrets:
        reddit = praw.Reddit(
            client_id=st.secrets["reddit"]["client_id"],
            client_secret=st.secrets["reddit"]["client_secret"],
            user_agent=st.secrets["reddit"]["user_agent"]
        )
        for keyword in keywords:
            subreddit = reddit.subreddit("all")
            for post in subreddit.search(keyword, sort="new", time_filter="week", limit=limit):
                if datetime.datetime.utcfromtimestamp(post.created_utc) > end_date:
                    posts.append({
                        "title": post.title,
                        "text": post.selftext,
                        "url": post.url,
                        "source": "reddit"
                    })
    else:
        # מצב 2: אין Reddit API → שימוש ב-Google Web Search
        for keyword in keywords:
            df = fetch_websearch(f"site:reddit.com {keyword}", limit=limit)
            if not df.empty:
                df["source"] = "reddit-google"
                posts.extend(df.to_dict("records"))

    return pd.DataFrame(posts)
