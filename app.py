import streamlit as st
import pandas as pd

from fetch_reddit import fetch_reddit_posts
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_problem
from daily_trends import fetch_daily_trends

st.set_page_config(page_title="Multi-Source Problem Finder → Product Ideas", layout="wide")
st.title("Multi-Source Problem Finder → Product Ideas (AliExpress + Trend Check + Daily Top 10)")

# פונקציה להצגת מוצרים בצורה נקייה
def display_products(products):
    st.subheader("מוצרים מומלצים:")
    for idx, p in enumerate(products, start=1):
        st.write(f"**{idx}. {p['name']}** – התאמה {p['match']}% – [🔗 לחץ כאן]({p['link']})")
        if p.get("desc"):
            st.caption(p["desc"])

# חיפוש מותאם אישית לפי מילת מפתח
topic = st.text_input("מה הבעיה או התחום שתרצה לחפש?")
if st.button("חפש פתרונות"):
    if topic.strip():
        st.write(f"מחפש בעיות עם מילת מפתח: {topic} ...")

        # מקורות שונים (Reddit, Google Trends, TikTok, Quora)
        reddit_df = fetch_reddit_posts(["BuyItForLife", "LifeProTips"], keyword=topic, days=7, limit=5)
        trends_df = fetch_google_trends(topic)
        tiktok_df = fetch_websearch(topic, site="tiktok.com", limit=3)
        quora_df = fetch_websearch(topic, site="quora.com", limit=3)

        combined = pd.concat([reddit_df, trends_df, tiktok_df, quora_df], ignore_index=True)
        combined = merge_and_filter(combined)

        if combined.empty:
            st.warning("לא נמצאו פוסטים רלוונטיים")
        else:
            st.write("נמצאו בעיות חוזרות שזוהו:")
            st.write(combined["text_clean"].unique().tolist())

            # ניתוח פתרונות
            recommended_products = analyze_problem(topic)
            if recommended_products:
                display_products(recommended_products)
            else:
                st.error("לא נמצאו מוצרים רלוונטיים לבעיה זו.")

# כפתור להצגת 10 בעיות טרנדיות (לא קשור למילת החיפוש)
if st.button("Top 10 בעיות טרנדיות השבוע"):
    st.write("בודק טרנדים כלליים...")
    daily_products = fetch_daily_trends()
    if daily_products:
        st.write("טופ 10 בעיות טרנדיות השבוע שניתן לפתור במוצר:")
        for idx, item in enumerate(daily_products, start=1):
            st.write(f"**{idx}. {item['problem']}** – [מוצר לדוגמה]({item['link']})")
            st.caption(item['desc'])
    else:
        st.warning("לא נמצאו טרנדים זמינים כרגע.")
