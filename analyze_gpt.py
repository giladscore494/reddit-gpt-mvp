import openai
import streamlit as st
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]

def analyze_problem(problem_text):
    """
    מבצע אנליזה לבעיה:
    1. מציע פתרון מהשורש (solution).
    2. מחזיר 3 מוצרים פיזיים רלוונטיים (רק מוצרים שניתן למצוא ב-AliExpress).
    3. מחזיר הסבר קצר לכל מוצר (explanation) ואחוז התאמה (match).
    הפלט מובטח להיות JSON בלבד.
    """

    prompt = f"""
הבעיה: {problem_text}

החזר אך ורק פלט בפורמט JSON הבא, ללא טקסט חופשי נוסף:
{{
  "solution":"גישה כללית לפתרון מהשורש",
  "products":[
    {{"product":"שם מוצר ראשון","match":95,"explanation":"למה המוצר מתאים"}},
    {{"product":"שם מוצר שני","match":90,"explanation":"למה המוצר מתאים"}},
    {{"product":"שם מוצר שלישי","match":85,"explanation":"למה המוצר מתאים"}}
  ]
}}

1. כתוב תחילה מה הדרך הטובה ביותר לפתור את הבעיה מהשורש (solution).
2. הצע 3 מוצרים פיזיים ספציפיים (רק מוצרים אמיתיים שאפשר למצוא ב-AliExpress).
3. הוסף לכל מוצר אחוז התאמה (match) והסבר קצר (explanation) למה הוא מתאים.
4. אל תוסיף שום טקסט נוסף מחוץ ל-JSON!
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        content = response.choices[0].message["content"].strip()

        # ניסיון לקרוא את הפלט כ-JSON
        result = json.loads(content)
        return result

    except json.JSONDecodeError:
        # אם הפלט לא היה JSON תקין
        return {
            "solution": "לא נמצא פתרון תקין",
            "products": []
        }
    except Exception as e:
        # בעיה אחרת (למשל ברשת או בהגדרות API)
        return {
            "solution": f"שגיאה: {str(e)}",
            "products": []
        }
