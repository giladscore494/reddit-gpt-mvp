from openai import OpenAI
import json

# יצירת לקוח OpenAI פעם אחת בלבד
client = OpenAI()

def analyze_problem(problem_text: str):
    """
    מקבל בעיה ומחזיר ניתוח מוצר (שם וקישור)
    """
    prompt = f"""
    הבעיה: "{problem_text}"
    מצא מוצר אחד בלבד שיכול לפתור את הבעיה הזו וודא שהוא מוצר פיזי שניתן לקנות.
    החזר פורמט JSON: 
    [{{"product": "שם מוצר", "match": 95, "link": "https://www.aliexpress.com/wholesale?SearchText=שם מוצר באנגלית"}}]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.4
        )

        raw = response.choices[0].message.content
        products = json.loads(raw)
        return products[0]["product"], products[0]["link"]

    except Exception as e:
        print("Error in GPT product analysis:", e)
        return "לא נמצא", "https://example.com"
