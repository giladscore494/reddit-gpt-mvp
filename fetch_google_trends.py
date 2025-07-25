import time
import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError

# Cache לשמירת תוצאות חיפושים שנעשו לאחרונה
_trends_cache = {}

def fetch_google_trends(keyword):
    """
    מביא נתוני מגמות מגוגל טרנדס לשבוע האחרון עבור מילה ספציפית.
    מחזיר DataFrame בפורמט אחיד עם עמודות: text_clean, source, title, url
    """
    # אם כבר חיפשנו את המילה, נחזיר מה־cache
    if keyword in _trends_cache:
        return _trends_cache[keyword]

    pytrends = TrendReq(hl='en-US', tz=360)

    try:
        # הגבלת קצב קריאות (כדי לא לקבל חסימה)
        time.sleep(2)
        pytrends.build_payload([keyword], timeframe='now 7-d')
        data = pytrends.interest_over_time()

        if data.empty:
            df = pd.DataFrame()
        else:
            # מחזירים שורה אחת שמציינת כי נמצאה מגמה
            df = pd.DataFrame([{
                "text_clean": keyword,
                "source": "GoogleTrends",
                "title": f"Google Trends interest for {keyword}",
                "url": f"https://trends.google.com/trends/explore?q={keyword}"
            }])

        _trends_cache[keyword] = df
        return df

    except TooManyRequestsError:
        print(f"Google Trends חסם את החיפוש על '{keyword}', חוזר ללא תוצאות")
        return pd.DataFrame()
    except Exception as e:
        print(f"שגיאת Google Trends ({keyword}): {e}")
        return pd.DataFrame()
