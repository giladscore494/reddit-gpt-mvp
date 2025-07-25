# analyze_gpt.py
from openai import OpenAI

# יצירת לקוח OpenAI פעם אחת בלבד
client = OpenAI()

def analyze_problem(problem_text: str):
    """
    מקבל בעיה (problem_text) ומחזיר ניתוח:
    product - רעיון לפתרון
    link - קישור מתאים (דמיוני כרגע)
    """
    try:
        # קריאה ל-OpenAI עם ה-API החדש
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "אתה עוזר לדרופשיפינג שמוצא בעיות ומייצר פתרונות."},
                {"role": "user", "content": f"מצא מוצר מתאים לבעיה הבאה: {problem_text} \
                והצג אותו בפורמט: מוצר: <שם מוצר>, קישור: <url>"}
            ],
            temperature=0.4
        )

        # פענוח תוצאה מהתשובה
        content = response.choices[0].message.content
        # פיצול פשוט – אפשר לשפר בהמשך
        if "קישור:" in content:
            product_part, link_part = content.split("קישור:")
            product = product_part.replace("מוצר:", "").strip()
            link = link_part.strip()
        else:
            product, link = content, "https://example.com"

        return product, link

    except Exception as e:
        # טיפול בשגיאות
        print(f"שגיאה בניתוח הבעיה: {e}")
        return "לא זמין", "https://example.com"
