from pytrends.request import TrendReq
import re

def fetch_daily_trends():
    """
    מחזיר את הטופ 10 החיפושים היומיים הפופולריים ביותר מגוגל טרנדס.
    מסנן רק מונחים שנראים כמו מוצרים פיזיים.
    """
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_today = pytrends.trending_searches(pn='united_states')
    product_trends = []

    for trend in trending_today[0].head(20):  # ניקח 20, אחר כך נסנן ל-10
        if is_product_like(trend):
            product_trends.append(trend)
        if len(product_trends) >= 10:
            break

    return product_trends

def is_product_like(query):
    """
    בדיקה בסיסית אם החיפוש נראה כמו מוצר (ולא שם של אדם/מקום).
    אפשר לשפר בעתיד עם GPT או רשימת קטגוריות.
    """
    banned_keywords = ["Netflix", "YouTube", "Facebook", "Trump", "Biden", "TikTok"]
    if any(word.lower() in query.lower() for word in banned_keywords):
        return False
    # אם יש מילה כללית של מוצר (watch, phone, shoes, car וכו')
    product_keywords = ["watch", "phone", "laptop", "shoes", "bag", "headphones", "tv", "camera", "printer"]
    return any(word in query.lower() for word in product_keywords) or bool(re.search(r"\d", query))
