import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_problem(problem_text):
    prompt = f"""
בעיה: {problem_text}

אנא הצע 5 מוצרים פיזיים מדויקים מאליאקספרס שיכולים לפתור את הבעיה.
לכל מוצר:
1. שם מדויק (באנגלית, כפי שהוא מופיע בדרך כלל באליאקספרס).
2. אחוז התאמה לבעיה (0–100%).

פורמט:
מוצר 1: <שם מוצר> | התאמה: <אחוז>
מוצר 2: <שם מוצר> | התאמה: <אחוז>
מוצר 3: <שם מוצר> | התאמה: <אחוז>
מוצר 4: <שם מוצר> | התאמה: <אחוז>
מוצר 5: <שם מוצר> | התאמה: <אחוז>
"""
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return resp.choices[0].message.content.strip()
