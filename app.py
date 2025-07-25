import streamlit as st
import pandas as pd

from fetch_reddit import fetch_reddit_posts
from fetch_websearch import fetch_websearch
from fetch_google_trends import fetch_google_trends
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_problem

st.title("Top 3 Hot Problems → AliExpress Solutions")

topic = st.text_input("כתבו תחום כללי (לדוגמה: אופנה, ספורט, טכנולוגיה)")

def heat_text(count):
    """קביעת מדד חום טקסטואלי"""
    if count >= 20:
        return f"נושא חם – מדובר רבות ברשת ({count}+ פוסטים בשבוע האחרון)"
    elif count >= 10:
        return f"נושא בינוני – יש עניין מתון ({count} פוסטים בשבוע האחרון)"
    else:
        return f"נושא עם מעט שיח – פחות מ-10 פוסטים ({count} פוסטים בשבוע האחרון)"

if st.button("חפש בעיות חמות"):
    # 1. איסוף נתונים
    reddit_df = fetch_reddit_posts([topic], days=7)
    quora_df = fetch_websearch(topic, site="quora.com", limit=5)
    trends_df = fetch_google_trends(topic)

    combined = merge_and_filter([reddit_df, quora_df, trends_df])
    
    if combined.empty:
        st.warning("לא נמצאו בעיות חמות לנושא זה השבוע.")
    else:
        # דירוג לפי הופעות (post_count)
        top3 = combined.sort_values("post_count", ascending=False).head(3)

        st.markdown("### 3 בעיות חמות והמוצרים שמומלץ למכור:")
        for i, row in enumerate(top3.itertuples(), start=1):
            st.write(f"**{i}. בעיה:** {row.title}")
            st.caption(heat_text(row.post_count))
            product, link = analyze_problem(row.title)
            st.write(f"**מוצר מוצע:** {product}")
            st.markdown(f"[🔗 לחץ כאן כדי לראות]({link})")

        st.info("💡 **מדד החום מבוסס על כמות פוסטים ברשת בשבוע האחרון – "
                "ככל שיש יותר שיח, כך הביקוש הפוטנציאלי גבוה יותר.**")
