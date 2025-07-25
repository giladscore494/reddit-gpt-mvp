import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_problem(problems_text):
    """
    מקבל רשימת בעיות (טקסט) ומחזיר:
    - בעיות מנותחות
    - פתרונות מוצעים
    - מוצרים עם התאמה ≥90% כולל קישור לאליאקספרס
    """
    prompt = f"""
    ניתנה לך רשימת בעיות שחוזרות ברשת:
    {problems_text}

    1. זהה את שלוש הבעיות המרכזיות בלבד.
    2. לכל בעיה הצע מוצר אחד בלבד מעלי אקספרס שיכול לפתור אותה עם התאמה ≥90%.
    3. החזר את התשובה במבנה JSON בלבד:
    [
      {{
        "problem": "שם הבעיה",
        "product": "שם מוצר",
        "link": "קישור אליאקספרס מדויק"
      }}
    ]
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()
    return content
