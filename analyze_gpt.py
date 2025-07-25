import openai
import streamlit as st
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_problem(problem_text):
    """
    אנליזה לבעיה:
    - מחזיר רשימת בעיות חוזרות שקשורות ישירות למוצרים פיזיים.
    - מחזיר 3 מוצרים פיזיים רלוונטיים לפתרון.
    - ללא פתרון מהשורש.
    """

    prompt = f"""
הבעיה: {problem_text}

החזר פלט JSON בלבד:
{{
  "problems":["בעיה 1","בעיה 2","בעיה 3"],
  "products":[
    {{"product":"שם מוצר ראשון","match":95,"explanation":"למה המוצר מתאים"}},
    {{"product":"שם מוצר שני","match":90,"explanation":"למה המוצר מתאים"}},
    {{"product":"שם מוצר שלישי","match":85,"explanation":"למה המוצר מתאים"}}
  ]
}}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message.content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return {"problems": [], "products": []}
    except Exception as e:
        return {"problems": [], "products": [], "error": str(e)}
