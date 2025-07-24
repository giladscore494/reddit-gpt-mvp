import requests
from bs4 import BeautifulSoup

def search_aliexpress(product_name):
    query = f"{product_name} site:aliexpress.com"
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    link = None
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "aliexpress.com" in href and "url?q=" in href:
            link = href.split("url?q=")[1].split("&")[0]
            break
    return link
