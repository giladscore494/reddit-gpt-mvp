import streamlit as st
import requests
import pandas as pd
import datetime

def fetch_twitter(query="problem", days=7, max_results=10):
    token = st.secrets["TWITTER_BEARER_TOKEN"]
    headers = {"Authorization": f"Bearer {token}"}
    since = (datetime.datetime.utcnow() - datetime.timedelta(days=days)).isoformat("T")+"Z"
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={max_results}&start_time={since}&tweet.fields=created_at,text"
    r = requests.get(url, headers=headers)
    data = r.json()
    tweets = []
    if "data" in data:
        for tw in data["data"]:
            tweets.append({
                "source": "Twitter",
                "title": tw["text"][:60],
                "text": tw["text"],
                "url": f"https://twitter.com/i/web/status/{tw['id']}"
            })
    return pd.DataFrame(tweets)
