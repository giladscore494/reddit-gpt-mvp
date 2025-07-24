import requests
import pandas as pd

def fetch_websearch(query, site="tiktok.com", num=5):
    q = f"site:{site} {query}"
    url = f"https://duckduckgo.com/html/?q={q}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    results = []
    for line in r.text.split('<a rel="nofollow" class="result__a" href="')[1:]:
        link = line.split('"')[0]
        results.append({
            "source": f"Web ({site})",
            "title": query,
            "text": f"Found result for {query}",
            "url": link
        })
        if len(results) >= num:
            break
    return pd.DataFrame(results)
