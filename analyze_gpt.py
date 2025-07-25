import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_and_find_products(problem):
    """
    שולח את הבעיה ל-GPT ומבקש פתרונות מוצר עם התאמה ≥ 90%.
    """
    prompt = f"""
    הבעיה: "{problem}"
    מצא מוצר אחד בלבד שיכול לפתור את הבעיה הזו וודא שהוא מוצר פיזי שניתן לקנות.
    החזר פורמט JSON: 
    [{{"product": "שם מוצר", "match": 95, "link": "https://www.aliexpress.com/wholesale?SearchText=שם מוצר באנגלית"}}]
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.4
        )

        raw = response.choices[0].message["content"]
        import json
        products = json.loads(raw)
        return products
    except Exception as e:
        print("Error in GPT product analysis:", e)
        return []
