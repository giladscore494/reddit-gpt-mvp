import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_topics_and_problems, analyze_solutions
from fetch_google_link import search_aliexpress

st.title("Multi-Source Problem Finder → Product Ideas (Optimized)")

keyword = st.text_input("מה הבעיה או התחום שתרצה לחפש?", "")

if st.button("Collect & Analyze"):
    if not keyword.strip():
        st.warning("אנא הזן מילה או תחום לחיפוש.")
    else:
        st.write(f"מחפש בעיות עם מילת מפתח: **{keyword}** ...")

        # --- GPT שלב ראשון: תתי נושאים ---
        subtopics = analyze_topics_and_problems(keyword)
        st.write(f"תתי נושאים לחיפוש: {', '.join(subtopics)}")

        # --- איסוף מידע מכל הפלטפורמות ---
        all_posts = []
        for topic in subtopics:
            reddit_df = fetch_reddit_posts(
                ["BuyItForLife", "LifeProTips"], keyword=topic, days=7, limit=5
            )
            trends_df = fetch_google_trends(topic)
            quora_df = fetch_websearch(topic, site="quora.com", limit=3)
            tiktok_df = fetch_websearch(topic, site="tiktok.com", limit=3)
            all_posts.append(pd.concat([reddit_df, trends_df, quora_df, tiktok_df], ignore_index=True))

        combined = pd.concat(all_posts, ignore_index=True)
        combined = merge_and_filter([combined])

        if combined.empty:
            st.warning("לא נמצאו מספיק נתונים לחיפוש הזה.")
        else:
            st.write(f"נמצאו {len(combined)} פוסטים לניתוח.")

            # --- GPT שלב שני: בעיות חוזרות ---
            problems = analyze_topics_and_problems(
                keyword, combined["text_clean"].tolist(), mode="problems"
            )
            st.write("**בעיות חוזרות שזוהו:**", problems)

            # --- GPT שלב שלישי: פתרונות ---
            solutions = analyze_solutions(problems)
            st.write("**GPT raw output:**", solutions)

            # --- הצגת מוצרים (3 בלבד) עם קישורים ---
            rows = []
            for solution in solutions:
                product_name = solution["product"]
                score = solution["match"]
                link = search_aliexpress(product_name)
                rows.append({
                    "Product": f"**{product_name}**",
                    "Match": f"{score}%",
                    "Link": f"[🔗 View Product]({link})"
                })

            output_df = pd.DataFrame(rows)
            st.write("### Recommended Products")
            st.write(output_df.to_html(escape=False, index=False), unsafe_allow_html=True)
            st.download_button("Download CSV", output_df.to_csv(index=False), "output.csv")
