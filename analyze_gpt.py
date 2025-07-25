import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator

# --- אתחול לקוח OpenAI ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def translate_if_needed(text):
    """
    מתרגם לעברית → אנגלית אם נדרש
    """
    if any("\u0590" <= c <= "\u05EA" for c in text):
        try:
            return GoogleTranslator(source='auto', target='en').translate(text)
        except Exception:
            return text  # fallback אם אין תרגום
    return text

def analyze_problem(problem_text):
    """
    ניתוח בעיה → הצעת מוצרים עם אנלוגיות והבנת מטרות
    """
    problem_english = translate_if_needed(problem_text)

    prompt = f"""
    You are a product research assistant.

    Problem: "{problem_english}"

    1. Understand what the person actually wants to achieve (Goal).
       Example: "nail polish is peeling" → Goal might be "make nail polish last longer".
    2. Suggest **exactly 5 PHYSICAL products** from AliExpress that directly or indirectly solve the problem.
    3. Each product must be practical, buyable, and highly relevant.
    4. Assign a **match score (0-100%)** based on how well it solves the problem.
    5. Be concise and specific (use product names likely to appear on AliExpress).

    Output format:
    Goal: <short description of goal>
    Product 1: <Exact Product Name> | Match: <Score>%
    Product 2: <Exact Product Name> | Match: <Score>%
    Product 3: <Exact Product Name> | Match: <Score>%
    Product 4: <Exact Product Name> | Match: <Score>%
    Product 5: <Exact Product Name> | Match: <Score>%
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
