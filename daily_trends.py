from pytrends.request import TrendReq
from fetch_google_link import search_aliexpress
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def fetch_weekly_problems():
    """
    מחזיר רשימת 10 בעיות פופולריות מהשבוע האחרון
    שאפשר לפתור עם מוצר מאלי אקספרס.
    """
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        trending_today = pytrends.trending_searches(pn='united_states')
        keywords = trending_today[0].tolist()[:10]
    except Exception:
        return []

    prompt = f"""
    Given these trending topics: {keywords}
    Identify if each represents a problem that can be solved by a product.
    If not, skip it. 
    For each valid problem, suggest one AliExpress product to solve it.
    Output as JSON list of objects with keys: problem, product.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        output_text = response.choices[0].message.content
    except Exception:
        return []

    results = []
    for line in output_text.splitlines():
        if "problem" in line.lower() and "product" in line.lower():
            try:
                # חיתוך פשוט – בלי תלות בפורמט מדויק
                parts = line.split("product:")
                problem = parts[0].replace("problem:", "").strip()
                product = parts[1].strip()
                link = search_aliexpress(product)
                results.append({"problem": problem, "link": link})
            except:
                continue

    return results
