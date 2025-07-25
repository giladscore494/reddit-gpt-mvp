import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from daily_trends import fetch_daily_trends
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_problem, analyze_and_find_products
from fetch_google_link import search_aliexpress

st.set_page_config(page_title="Multi-Source Problem Finder → Product Ideas (AliExpress + Trend Check)", layout="wide")
st.title("Multi-Source Problem Finder → Product Ideas (AliExpress + Trend Check + Daily Top 10)")

# --- קלט מהמשתמש ---
topic = st.text_input("מה הבעיה או התחום שתרצה לחפש?", "")

# --- כפתור טרנדים עולמיים ---
if st.button("הצג 10 בעיות טרנדיות בשבוע האחרון"):
    trending_problems = analyze_problem("top trending problems globally")
    st.subheader("10 בעיות טרנדיות שניתן לפתור עם מוצרי AliExpress")
    for idx, item in enumerate(trending_problems, 1):
        if isinstance(item, dict):
            problem = item.get("problem", "לא זמין")
            link = item.get("link", "#")
            st.markdown(f"**{idx}. {problem}** – [מוצר לדוגמה]({link})", unsafe_allow_html=True)
        else:
            st.markdown(f"**{idx}. {item}**", unsafe_allow_html=True)

# --- עיבוד חיפוש מותאם אישית ---
if st.button("בצע חיפוש מותאם"):
    if topic.strip() == "":
        st.warning("אנא הזן תחום או בעיה לחיפוש.")
    else:
        st.write(f"מחפש בעיות עם מילת מפתח: **{topic}** ...")

        # חיפושים ממקורות שונים
        reddit_df = fetch_reddit_posts(["BuyItForLife", "LifeProTips"], keyword=topic, days=7, limit=5)
        trends_df = fetch_google_trends(topic)
        web_df = fetch_websearch(topic, site="quora.com", limit=3)

        # מיזוג וסינון
        combined = merge_and_filter([reddit_df, trends_df, web_df])

        if combined.empty:
            st.warning("לא נמצאו בעיות מספיק חמות או עם נפח חיפוש גבוה.")
        else:
            # ניתוח עם GPT למציאת מוצרים מתאימים
            problems = combined["title"].tolist()
            top_problem = problems[0] if problems else topic
            st.write("**בעיות חוזרות שזוהו:**")
            for p in problems[:5]:
                st.markdown(f"- {p}")

            st.subheader("פתרון מהשורש:")
            root_solution, recommended_products = analyze_and_find_products(top_problem)

            st.write(root_solution if root_solution else "לא נמצאה תשובה תקינה")

            st.subheader("מוצרים מומלצים:")
            if recommended_products:
                for prod in recommended_products:
                    name = prod.get("product", "מוצר לא ידוע")
                    match = prod.get("match", 0)
                    desc = prod.get("description", "")
                    link = search_aliexpress(name)
                    st.markdown(
                        f"""
                        <div style="margin-bottom:20px; padding:10px; border:1px solid #ddd; border-radius:8px;">
                            <b>{name}</b> – התאמה {match}%<br>
                            <span style="color:gray;font-size:14px">{desc}</span><br>
                            <a href="{link}" target="_blank"
                               style="color:white;background:#0073e6;padding:5px 10px;
                               border-radius:5px;text-decoration:none;display:inline-block;margin-top:5px;">
                               🔗 לחץ כאן
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.write("לא נמצאו מוצרים מתאימים.")

        # הצגת מוצרים טרנדיים (Top 10) באופן כללי
        st.subheader("טופ 10 מוצרים פופולריים היום (Google Trends):")
        try:
            daily_products = fetch_daily_trends()
            if not daily_products.empty:
                st.table(daily_products)
            else:
                st.write("Fallback: No live Google Trends available")
        except Exception as e:
            st.error(f"שגיאה בטעינת Google Trends: {e}")
