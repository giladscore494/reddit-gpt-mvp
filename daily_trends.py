import requests
import xml.etree.ElementTree as ET
import re

RSS_URL = "https://trends.google.com/trends/trendingsearches/daily/rss?geo=US"

def fetch_daily_trends():
    """
    מושך את הטופ 10 חיפושים יומיים מגוגל טרנדס (גרסת RSS).
    מחזיר רשימת מונחים שנראים כמו מוצרים פיזיים בלבד.
    """
    try:
        r = requests.get(RSS_URL, timeout=5)
        if r.status_code == 200:
            root = ET.fromstring(r.content)
            items = root.findall(".//item/title")
            terms = [t.text for t in items if t.text]
            product_terms = []
            for term in terms:
                if is_product_like(term):
                    product_terms.append(term)
                if len(product_terms) >= 10:
                    break
            return product_terms
    except Exception:
        pass

    # fallback במקרה של כשל
    return ["Fallback: No live Google Trends available"]

def is_product_like(query):
    """
    בדיקה בסיסית אם החיפוש נראה כמו מוצר (ולא שם של אדם/מקום).
    """
    banned_keywords = ["Netflix", "YouTube", "Facebook", "Trump", "Biden", "TikTok"]
    if any(word.lower() in query.lower() for word in banned_keywords):
        return False
    product_keywords = [
        "watch", "phone", "laptop", "shoes", "bag", "headphones", "tv",
        "camera", "printer", "sofa", "desk", "table", "jacket"
    ]
    return any(word in query.lower() for word in product_keywords) or bool(re.search(r"\d", query))
