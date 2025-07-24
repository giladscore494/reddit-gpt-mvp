import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_problem(problem_text):
    prompt = f"""
    בעיה פופולרית:
    {problem_text}

    הצע 3 מוצרים פיזיים שאפשר למכור בדרופשיפינג שיכולים לפתור את הבעיה.
    הסבר בקצרה לכל מוצר למה הוא פותר את הבעיה.
    הפלט בעברית.
    """
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()
