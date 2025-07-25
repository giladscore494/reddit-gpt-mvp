import streamlit as st
from openai import OpenAI

# אתחול לקוח OpenAI עם מפתח מה-Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_problem(problem_text):
    prompt = f"""
    You are a product research assistant.

    If the input is in Hebrew, first translate it into English for research,
    but always output product names in English (as found on AliExpress).

    Task:
    1. Find exactly 5 physical products from AliExpress that solve the problem: "{problem_text}".
    2. All products must be highly relevant to this problem (ignore unrelated categories completely).
    3. For each product, give:
       - Exact product name (as found on AliExpress)
       - Match score (0-100%)

    Output format:
    Product 1: <Product Name> | Match: <Score>%
    Product 2: <Product Name> | Match: <Score>%
    Product 3: <Product Name> | Match: <Score>%
    Product 4: <Product Name> | Match: <Score>%
    Product 5: <Product Name> | Match: <Score>%
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,   # <<< מגבלת טוקנים
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
