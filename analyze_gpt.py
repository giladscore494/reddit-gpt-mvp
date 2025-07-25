import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_problem(problem_text):
    """
    מבצע אנליזה לבעיה:
    1. מגדיר את הדרך הטובה ביותר לפתור את הבעיה (מהשורש).
    2. ממליץ על 3 מוצרים רלוונטיים (רק מוצרים פיזיים מאתר AliExpress).
    3. מוסיף הסבר קצר למה כל מוצר מתאים.
    """
    prompt = f"""
    הבעיה: {problem_text}

    1. הסבר בקצרה מה הדרך הטובה ביותר לפתור בעיה זו מהשורש (גישה כללית).
    2. לאחר מכן, הצע 3 מוצרים פיזיים ספציפיים מאתר AliExpress שעשויים לעזור.
    3. עבור כל מוצר כתוב:
       - שם מוצר ברור
       - אחוז התאמה (מספר שלם)
       - הסבר קצר למה הוא מתאים
       - ציין שם מלא כדי שאפשר יהיה לחפש אותו ישירות באליאקספרס
    הפלט חייב להיות בפורמט JSON לדוגמה:
    {{
        "solution":"גישה כללית...",
        "products":[
            {{"product":"שם מוצר","match":95,"explanation":"למה מתאים"}},
            {{"product":"שם מוצר","match":90,"explanation":"למה מתאים"}},
            {{"product":"שם מוצר","match":85,"explanation":"למה מתאים"}}
        ]
    }}
    """
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    import json
    try:
        content = response.choices[0].message["content"]
        return json.loads(content)
    except Exception:
        return {"solution":"לא נמצאה תשובה תקינה","products":[]}

