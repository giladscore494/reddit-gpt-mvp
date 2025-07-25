import streamlit as st
import pandas as pd
from daily_trends import get_combined_trends
from fetch_websearch import fetch_forum_posts
from analyze_gpt import analyze_problem

st.title("Trend → Product Finder")

domain = st.text_input("הזן תחום כללי (לדוגמה: טכנולוגיה, אופנה, רכב)", "טכנולוגיה")

if st.button("אתר טרנדים והצע מוצרים"):
    with st.spinner("מזהה בעיות טרנדיות..."):
        trends_df = get_combined_trends(domain)
    if trends_df.empty:
        st.warning("לא נמצאו נושאים חמים.")
    else:
        st.subheader("נושאים חמים שנמצאו:")
        st.dataframe(trends_df)

        results = []
        for _, row in trends_df.iterrows():
            problem = row["topic"]
            posts_count = row["posts_count"]
            heat = row["heat"]

            # ניתוח מוצר
            product, link = analyze_problem(problem)
            results.append({
                "בעיה": problem,
                "כמות פוסטים": posts_count,
                "דרגת חום": heat,
                "מוצר מוצע": product,
                "קישור": link
            })

        st.subheader("תוצאות סופיות:")
        results_df = pd.DataFrame(results)
        st.dataframe(results_df)
        st.download_button("הורד CSV", results_df.to_csv(index=False), "results.csv")
