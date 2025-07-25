import openai
from deep_translator import GoogleTranslator
import streamlit as st
from fetch_google_link import search_aliexpress

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_problem(problem_text):
    """
    מתרגם בעיה, מבצע אנלוגיה למציאת מוצר מתאים ב-90%+ התאמה.
    """
    translated = GoogleTranslator(source='auto', target='en').translate(problem_text)

    prompt = f"""
You are a product sourcing expert. A user problem is described: "{translated}".
Find ONE AliExpress product that solves it effectively. 
Return product name only, 90%+ match required.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.4
    )

    product_name = response.choices[0].message["content"].strip()
    link = search_aliexpress(product_name)
    return product_name, link
