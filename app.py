import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from merge_and_filter import merge_and_filter
from daily_trends import fetch_weekly_problems
from analyze_gpt import analyze_and_find_products  # חדש

st.set_page_config(page_title="Multi-Source Problem Finder → Product Ideas (AliExpress)", layout="wide")
st.title("Multi-Source Problem Finder → Product Ideas (AliExpress Only)")

topic = st.text_input("מה הבעיה או התחום שתרצה לחפש?")
min_posts = st.number_input("מינימום פוסטים בשבוע האחרון", min_value=1, value=5)
min_interactions = st.number_input("מינימום אינטראקציות ממוצעות לפוסט", min_value=1, value=10)

if st.button("חפש"):
    if not topic.strip():
        st.warning("אנא הזן נושא לחיפוש")
    else:
        st.info(f"מחפש בעיות עם מילת מפתח: {topic} ...")

        # איסוף נתונים
        reddit_df = fetch_reddit_posts(["BuyItForLife", "LifeProTips"], keyword=topic, days=7, limit=10)
        trends_df = fetch_google_trends(topic)
        quora_df = fetch_websearch(topic, site="quora.com", limit=3)

        combined = merge_and_filter([reddit_df, trends_df, quora_df])

        if combined.empty:
            st.warning("לא נמצאו בעיות בוערות בנושא הזה.")
        else:
            st.success(f"נמצאו {len(combined)} פוסטים לניתוח.")
            problems, products = analyze_and_find_products(combined)

            st.subheader("בעיות חוזרות שזוהו:")
            for p in problems:
                st.write(f"- {p}")

            st.subheader("מוצרים מומלצים:")
            for item in products:
                st.markdown(f"""
                <div style="margin-bottom:20px; padding:10px; border:1px solid #ddd; border-radius:8px;">
                    <b>{item['product']}</b> – התאמה {item['match']}%<br>
                    <span style="color:gray;font-size:14px">{item['desc']}</span><br>
                    <a href="{item['link']}" target="_blank"
                       style="color:white;background:#0073e6;padding:5px 10px;
                       border-radius:5px;text-decoration:none;display:inline-block;margin-top:5px;">
                       🔗 לחץ כאן
                    </a>
                </div>
                """, unsafe_allow_html=True)

# כפתור לתצוגת טופ 10 בעיות פופולריות
if st.button("הצג 10 בעיות פופולריות השבוע"):
    top_problems = fetch_weekly_problems()
    if top_problems:
        st.subheader("10 בעיות פופולריות השבוע שניתן לפתור עם מוצר:")
        for idx, item in enumerate(top_problems, 1):
            st.write(f"**{idx}. {item['problem']}** – [מוצר לדוגמה]({item['link']})")
    else:
        st.warning("לא נמצאו בעיות פופולריות לשבוע זה.")
