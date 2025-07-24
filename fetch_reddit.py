import streamlit as st
import praw
import pandas as pd
import datetime

def fetch_reddit_posts(subreddits, days=7, limit=20):
    reddit = praw.Reddit(
        client_id=st.secrets["REDDIT_CLIENT_ID"],
        client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
        user_agent=st.secrets["REDDIT_USER_AGENT"]
    )

    cutoff = datetime.datetime.utcnow().timestamp() - days*24*60*60
    posts_data = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.new(limit=limit):
            if post.created_utc >= cutoff:
                text = (post.title + " " + post.selftext).strip()
                posts_data.append({
                    "source": "Reddit",
                    "title": post.title,
                    "text": text,
                    "url": post.url
                })
    return pd.DataFrame(posts_data)
