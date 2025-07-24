import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_post(title, text):
    prompt = f"""
    פוסט מרדיט:
    כותרת: {title}
    תוכן: {text}

    1. מה הבעיה העיקרית שהפוסט מתאר?
    2. הצע 3 מוצרים פיזיים שאפשר למכור (דרופשיפינג) שיכולים לפתור את הבעיה.
    3. עבור כל מוצר, הסבר בקצרה למה הוא פותר את הבעיה.
    הפלט בעברית.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
