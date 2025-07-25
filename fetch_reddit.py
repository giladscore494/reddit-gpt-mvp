import requests
import pandas as pd
import time

# -------- אפשרות שימוש ב-PRAW כגיבוי --------
try:
    import praw
    USE_PRAW = True
except ImportError:
    USE_PRAW = False

# ---- פונקציה עיקרית ----
def fetch_reddit_posts(keywords, days=7, use_pushshift=True, praw_client=None):
    """
    מחזיר פוסטים לפי מילות מפתח מ-Reddit.
    ברירת מחדל: Pushshift API (לא מוגבל כמעט).
    אם use_pushshift=False או Pushshift לא עבד → PRAW (דורש client).
    """
    if use_pushshift:
        try:
            return fetch_from_pushshift(keywords, days)
        except Exception as e:
            print(f"Pushshift API error: {e}")
            if USE_PRAW and praw_client:
                return fetch_from_praw(keywords, praw_client)
            else:
                return pd.DataFrame()
    else:
        if USE_PRAW and praw_client:
            return fetch_from_praw(keywords, praw_client)
        else:
            print("PRAW client not available!")
            return pd.DataFrame()


def fetch_from_pushshift(keywords, days=7):
    """
    חיפוש ב-Pushshift (ללא מפתח)
    """
    query = " ".join(keywords)
    url = f"https://api.pushshift.io/reddit/search/submission/?q={query}&after={days}d&size=50"
    response = requests.get(url, timeout=10)
    data = response.json().get("data", [])
    if not data:
        return pd.DataFrame()
    posts = [
        {
            "title": p.get("title", ""),
            "text": p.get("selftext", ""),
            "score": p.get("score", 0),
            "subreddit": p.get("subreddit", "")
        }
        for p in data
    ]
    return pd.DataFrame(posts)


def fetch_from_praw(keywords, praw_client):
    """
    חיפוש עם PRAW (דורש client_id, client_secret, user_agent)
    """
    posts = []
    for kw in keywords:
        subreddit = praw_client.subreddit("all")
        for post in subreddit.search(kw, limit=50):
            posts.append({
                "title": post.title,
                "text": post.selftext,
                "score": post.score,
                "subreddit": str(post.subreddit)
            })
            time.sleep(1)  # הגבלת קצב כדי לא להיחסם
    return pd.DataFrame(posts)
