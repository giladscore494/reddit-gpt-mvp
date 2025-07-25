from pytrends.request import TrendReq
import requests

def check_google_trends(keyword):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword])
        data = pytrends.interest_over_time()
        if not data.empty:
            score = int(data[keyword].mean())
            return score
    except Exception:
        return 0
    return 0

def check_reddit_mentions(keyword):
    url = f"https://www.reddit.com/search.json?q={keyword}&limit=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            json_data = r.json()
            posts = json_data.get("data", {}).get("children", [])
            return len(posts)
    except Exception:
        return 0
    return 0

def get_trend_score(product_name):
    google_score = check_google_trends(product_name)
    reddit_mentions = check_reddit_mentions(product_name)
    total_score = google_score + (reddit_mentions * 5)
    if total_score > 50:
        return "🔥 טרנדי"
    elif total_score > 20:
        return "ביקוש בינוני"
    else:
        return "נמוך"
