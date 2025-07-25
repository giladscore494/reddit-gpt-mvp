import requests
from bs4 import BeautifulSoup
import urllib.parse

def search_aliexpress(product_name):
    """
    חיפוש מוצר באליאקספרס לפי שם מדויק, מחזיר קישור לחיץ.
    אם לא נמצאה תוצאה ישירה → מחזיר קישור חיפוש בסיסי.
    """
    query = urllib.parse.quote_plus(product_name)
    search_url = f"https://www.aliexpress.com/wholesale?SearchText={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(search_url, headers=headers, timeout=5)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            first_link = soup.select_one("a[href*='item']")
            if first_link and first_link.get("href"):
                link = first_link.get("href")
                if not link.startswith("http"):
                    link = "https:" + link
                return link
    except Exception:
        pass

    # fallback: החזרת קישור חיפוש ישיר
    return search_url
