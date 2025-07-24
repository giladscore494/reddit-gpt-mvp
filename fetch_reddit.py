import streamlit as st
import praw
import pandas as pd

def fetch_reddit_posts(subreddits, limit=5):
    reddit = praw.Reddit(
        client_id=st.secrets["REDDIT_CLIENT_ID"],
        client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
        user_agent=st.secrets["REDDIT_USER_AGENT"]
    )

    posts_data = []
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for post in subreddit.hot(limit=limit):
            posts_data.append({
                "subreddit": sub,
                "title": post.title,
                "text": post.selftext,
                "url": post.url
            })

    return pd.DataFrame(posts_data)
