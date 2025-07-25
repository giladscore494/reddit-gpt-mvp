from pytrends.request import TrendReq
from fetch_google_link import search_aliexpress
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def fetch_top3_products_by_topic(user_topic):
    """
    מקבל תחום כללי (כמו אופנה / ספורט / טכנולוגיה)
    ומחזיר 3 מוצרים רלוונטיים ביותר לבעיות שעלו בשבוע האחרון.
    """
    # --- חיפוש 3 נושאים חמים לפי Google Trends ---
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending = pytrends.trending_searches(pn='united_states')
        # סינון לנושאים הקשורים לתחום המשתמש
        filtered = [t for t in trending[0].tolist() if user_topic.lower() in t.lower()][:3]
        if len(filtered) < 3:
            # fallback - פשוט לקחת 3 ראשונים
            filtered = trending[0].tolist()[:3]
    except Exception:
        filtered = [f"{user_topic} issue {i}" for i in range(1, 4)]

    # --- GPT אנלוגיה + פתרונות ---
    prompt = f"""
    The topic is: {user_topic}.
    Trending issues this week: {filtered}.
    For each issue:
    1. Summarize the main problem.
    2. Suggest one AliExpress product that can best solve it.
    Return only 3 results in format: problem | product.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        output_text = response.choices[0].message.content
    except Exception:
        return []

    results = []
    for line in output_text.splitlines():
        if "|" in line:
            try:
                problem, product = line.split("|", 1)
                problem, product = problem.strip(), product.strip()
                link = search_aliexpress(product)
                results.append({
                    "problem": problem,
                    "product": product,
                    "link": link
                })
            except:
                continue

    return results[:3]
