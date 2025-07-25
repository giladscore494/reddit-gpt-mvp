import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

def fetch_forum_posts(query, num_results=20):
    """
    חיפוש בגוגל בפורומים (Quora + StackExchange)
    """
    query += ' site:quora.com OR site:stackexchange.com'
    query = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query}&num={num_results}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for g in soup.select(".tF2Cxc"):
        title = g.select_one("h3").text if g.select_one("h3") else "No title"
        link = g.select_one("a")["href"] if g.select_one("a") else ""
        snippet = g.select_one(".VwiC3b").text if g.select_one(".VwiC3b") else ""
        results.append({"title": title, "link": link, "snippet": snippet})

    return pd.DataFrame(results)
