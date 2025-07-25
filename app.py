import streamlit as st
import pandas as pd
from daily_trends import get_combined_trends
from analyze_gpt import analyze_problem

st.title("Trend → Product Finder")

domain = st.text_input("הזן תחום כללי (לדוגמה: טכנולוגיה, אופנה, רכב)", "טכנולוגיה")

if st.button("אתר טרנדים והצע מוצרים"):
    with st.spinner("מזהה בעיות טרנדיות..."):
        trends_df = get_combined_trends(domain)

    if trends_df.empty:
        st.warning("לא נמצאו נושאים חמים.")
    else:
        # בחירת 3 נושאים הכי חמים
        top_trends = trends_df.sort_values(by="posts_count", ascending=False).head(3).reset_index(drop=True)

        results = []
        for _, row in top_trends.iterrows():
            problem = row["topic"]
            posts_count = row["posts_count"]
            heat = row["heat"]

            # קריאת GPT למציאת מוצר
            product, link = analyze_problem(problem)
            results.append({
                "בעיה": problem,
                "כמות פוסטים": posts_count,
                "דרגת חום": heat,
                "מוצר מוצע": product,
                "קישור למוצר": link
            })

        # הצגת התוצאות
        st.subheader("3 בעיות הכי חמות והמוצרים המוצעים:")
        results_df = pd.DataFrame(results)
        st.dataframe(results_df)
        st.download_button("הורד CSV", results_df.to_csv(index=False), "results.csv")
