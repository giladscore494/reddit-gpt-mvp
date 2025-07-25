import streamlit as st
import praw
import pandas as pd
from datetime import datetime, timedelta

def fetch_reddit_posts(subreddits, keyword=None, days=7, limit=10):
    reddit = praw.Reddit(
        client_id=st.secrets["REDDIT_CLIENT_ID"],
        client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
        user_agent="reddit-problem-finder"
    )

    posts = []
    after_timestamp = int((datetime.utcnow() - timedelta(days=days)).timestamp())

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.new(limit=50):
            if post.created_utc < after_timestamp:
                continue

            text = f"{post.title} {post.selftext}"
            if keyword and keyword.lower() not in text.lower():
                continue

            posts.append({
                "title": post.title,
                "text": post.selftext,
                "score": post.score,
                "text_clean": text
            })

            if len(posts) >= limit:
                break

    return pd.DataFrame(posts)
