import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator
from fetch_google_link import search_aliexpress

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_problem(problem_text):
    """
    מנתח בעיה ומחזיר:
    - רשימת מוצרים (שם, אחוז התאמה, תיאור, קישור עלי אקספרס)
    """
    # תרגום לאנגלית לשיפור הבנת GPT
    translated_problem = GoogleTranslator(source='auto', target='en').translate(problem_text)

    prompt = f"""
You are a product solution expert.
Given the following user problem: "{translated_problem}"

1. Suggest 3-5 physical products that can effectively solve this problem.
2. For each product, provide:
   - Product name (short)
   - Short description (1 sentence)
   - Match percentage (0-100)

Return as JSON list:
[{{"name": "...", "desc": "...", "match": 90}}, ...]
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a product solution AI."},
                  {"role": "user", "content": prompt}],
        temperature=0.5
    )

    # ניתוח פלט JSON של GPT
    raw = response.choices[0].message.content.strip()
    import json
    try:
        products = json.loads(raw)
    except json.JSONDecodeError:
        return []

    # הוספת קישור עלי אקספרס לכל מוצר
    for p in products:
        p["link"] = search_aliexpress(p["name"])

    return products
