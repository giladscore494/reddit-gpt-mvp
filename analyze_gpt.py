import openai
import streamlit as st
from deep_translator import GoogleTranslator

openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception:
        return text

def analyze_problem(problem_text):
    """
    מפענח בעיה כללית ומחזיר תובנה בסיסית
    """
    translated = translate_to_english(problem_text)
    prompt = f"""
    Identify the root issue described here and summarize it in one short sentence:
    "{translated}"
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

def analyze_and_find_products(problem_text):
    """
    מזהה פתרונות מוצרים אפשריים מעלי אקספרס ומדרג אותם לפי התאמה.
    מחזיר רשימה עם מוצר, אחוז התאמה, ותיאור קצר.
    """
    translated = translate_to_english(problem_text)
    prompt = f"""
    The user described a problem: "{translated}".
    Your task:
    1. Suggest 3 concrete products that could solve this problem (physical items sold online, ideally from AliExpress).
    2. Rank them by relevance (percent 0-100).
    3. Provide a one-line reason for each.

    Respond in JSON array format like:
    [
      {{"product": "Product Name", "match": 95, "reason": "Why it helps"}},
      ...
    ]
    """
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content.strip()
