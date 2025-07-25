from openai import OpenAI
import json
import re

client = OpenAI()

def analyze_problem(problem_text: str):
    """
    מקבל בעיה ומחזיר מוצר מוצע עם קישור.
    """
    prompt = f"""
    בעיה: "{problem_text}"
    מצא מוצר פיזי אחד בלבד שיכול לפתור את הבעיה הזו.
    החזר JSON בלבד:
    [{{"product": "<שם מוצר>", "link": "<קישור חיפוש באנגלית ב-Aliexpress>"}}]
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.4
        )
        raw = response.choices[0].message.content
        json_match = re.search(r"\[.*\]", raw, re.S)
        products = json.loads(json_match.group(0)) if json_match else []
        product_name = products[0].get("product", "לא נמצא")
        link = products[0].get("link", f"https://www.aliexpress.com/wholesale?SearchText={product_name}")
        return product_name, link
    except Exception as e:
        print("Error in GPT product analysis:", e)
        return "לא נמצא", "https://www.aliexpress.com"
