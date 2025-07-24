import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_post(title, text):
    prompt = f"""
    פוסט מרדיט:
    כותרת: {title}
    תוכן: {text}

    מה הבעיה המרכזית שמתוארת כאן? הצג 3 פתרונות אפשריים.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
