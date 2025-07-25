from pytrends.request import TrendReq
import pandas as pd

def fetch_google_trends(keyword="fashion"):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], timeframe='now 7-d')

    data = pytrends.interest_over_time()
    data.reset_index(inplace=True)

    score = int(data[keyword].mean()) if not data.empty else 0
    return pd.DataFrame([{
        "title": f"Google Trends for {keyword}",
        "text": f"Interest over time last 7 days for {keyword}",
        "score": score,
        "text_clean": f"Google Trends interest for {keyword}"
    }])
