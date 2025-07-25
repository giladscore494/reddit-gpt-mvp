import streamlit as st
from openai import OpenAI

# אתחול לקוח OpenAI עם מפתח מה-Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_problem(problem_text):
    prompt = f"""
    You are a product research assistant.

    1. Understand what the user actually wants to achieve (goal).
       - If input is in Hebrew, translate it into English to understand the goal.
    2. Suggest exactly 5 PHYSICAL products from AliExpress
       that directly or indirectly solve the problem or help achieve the goal.
    3. Products should be practical, buyable, and highly relevant.
    4. Output must include match score (0-100%) that represents how well the product solves the goal.

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
