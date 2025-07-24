from pytrends.request import TrendReq
import pandas as pd

def fetch_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=["problem", "need help"], timeframe='now 7-d')
    interest_over_time = pytrends.interest_over_time()
    if interest_over_time.empty:
        return pd.DataFrame()
    topics = interest_over_time.mean().sort_values(ascending=False).head(5).index
    return pd.DataFrame([{"source": "GoogleTrends", "title": kw, "text": kw, "url": ""} for kw in topics])
