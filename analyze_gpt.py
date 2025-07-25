import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator
from fetch_google_link import search_aliexpress

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_and_find_products(df):
    """
    ניתוח בעיות והצעת מוצרים מאלי אקספרס
    """
    text = "\n".join(df["text_clean"].tolist())
    translated_text = GoogleTranslator(source='auto', target='en').translate(text)

    prompt = f"""
    Identify the top 3 recurring problems mentioned in the following text
    and suggest the best AliExpress products to solve them.
    Return results in JSON format with:
    - problems: list of problems
    - products: list of objects with keys [product, match, desc]
    Text: {translated_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    output_text = response.choices[0].message.content

    # פענוח פשוט (ללא JSON מלא)
    problems = []
    products = []

    for line in output_text.splitlines():
        if "problem" in line.lower():
            problems.append(line.strip())
        if "product" in line.lower():
            name = line.replace("product:", "").strip()
            link = search_aliexpress(name)
            products.append({
                "product": name,
                "match": 90,
                "desc": "מוצר מתאים שנמצא",
                "link": link
            })

    return problems, products
