import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_websearch(query, site=None, limit=3):
    """
    חיפוש בגוגל עם אופציה להגביל לאתר ספציפי
    - query: מילת חיפוש
    - site: (אופציונלי) אתר מסוים לחיפוש (למשל "quora.com")
    - limit: מספר תוצאות להחזיר
    """
    if site:
        query = f"site:{site} {query}"

    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for g in soup.select('a'):
        href = g.get('href')
        if href and "http" in href and "google.com" not in href:
            links.append(href)
            if len(links) >= limit:
                break

    return pd.DataFrame([{
        "title": f"Web search result {i+1}",
        "text": links[i],
        "score": 1,
        "text_clean": links[i]
    } for i in range(len(links))])
