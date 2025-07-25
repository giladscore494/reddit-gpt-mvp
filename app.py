import openai
import streamlit as st
from deep_translator import GoogleTranslator

# הגדרת מפתח OpenAI מהסודות
openai.api_key = st.secrets["OPENAI_API_KEY"]

def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception:
        return text

def analyze_problem(topic):
    """
    מחזיר 10 בעיות פופולריות שיכולות להיפתר ע"י מוצרי AliExpress.
    """
    prompt = f"""
    List 10 specific, recurring problems that people talk about online in the area of: {topic}.
    Only include problems that could realistically be solved using physical consumer products from sites like AliExpress.
    Format your answer as a numbered JSON list of dictionaries with 'problem' and 'link' (search URL on AliExpress using product name).
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6
        )
        text = response.choices[0].message.content.strip()

        # ניסיון לפרש את הפלט
        import json, re
        json_text = re.findall(r'\[(.*?)\]', text, re.DOTALL)
        if json_text:
            return json.loads(f"[{json_text[0]}]")
        else:
            # fallback: מחרוזות פשוטות
            lines = [line.strip("-•1234567890. ") for line in text.splitlines() if len(line.strip()) > 5]
            return lines[:10]
    except Exception:
        return []

def analyze_and_find_products(problem_text):
    """
    מקבל בעיה אחת, מחזיר פתרון שורש + רשימת מוצרים עם תיאור והתאמה.
    """
    translated = translate_to_english(problem_text)
    prompt = f"""
    Analyze the following problem: "{translated}"

    1. What is the most effective root-level solution to this problem? (briefly)
    2. Recommend 3–5 AliExpress-appropriate physical products that can help address this problem.
    For each product, return:
    - "product": name
    - "match": % match to the problem
    - "description": 1-sentence explanation

    Format your response as:
    ROOT: <root_solution>
    PRODUCTS:
    [{{"product": "...", "match": 90, "description": "..."}}]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        output = response.choices[0].message.content.strip()

        import re, json
        root_match = re.search(r'ROOT:\s*(.+?)\n', output)
        products_match = re.search(r'PRODUCTS:\s*\n(.+)', output, re.DOTALL)

        root_solution = root_match.group(1).strip() if root_match else "לא נמצאה תשובה תקינה"
        products_json = products_match.group(1).strip() if products_match else "[]"

        try:
            products = json.loads(products_json)
        except:
            # ניסיון לפענח רשימת שורות פשוטה
            products = []
            for line in products_json.splitlines():
                if ":" in line:
                    name = line.split(":")[0].strip("-•* ")
                    match = int(re.findall(r'\d+', line)[-1]) if re.findall(r'\d+', line) else 70
                    products.append({"product": name, "match": match, "description": ""})
        return root_solution, products
    except Exception:
        return "לא נמצאה תשובה תקינה", []
