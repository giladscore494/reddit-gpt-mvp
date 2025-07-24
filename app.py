import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_problem
from fetch_google_link import search_aliexpress

st.title("Multi-Source Problem Finder → Product Ideas")

keyword = st.text_input("מה הבעיה או התחום שתרצה לחפש?", "")

if st.button("Collect & Analyze"):
    if keyword.strip() == "":
        st.warning("אנא הזן מילה או תחום לחיפוש.")
    else:
        st.write(f"מחפש בעיות עם מילת מפתח: **{keyword}** ...")

        # שליפת נתונים
        reddit_df = fetch_reddit_posts(["BuyItForLife", "LifeProTips"], days=7)
        trends_df = fetch_google_trends()
        tiktok_df = fetch_websearch(keyword, site="tiktok.com")
        quora_df = fetch_websearch(keyword, site="quora.com")

        st.write(f"Reddit results: {len(reddit_df)}, Trends: {len(trends_df)}, TikTok: {len(tiktok_df)}, Quora: {len(quora_df)}")

        combined = merge_and_filter([reddit_df, trends_df, tiktok_df, quora_df])
        if combined.empty:
            st.warning("לא נמצאו בעיות עם מילת המפתח הזו.")
        else:
            results = []
            for _, row in combined.iterrows():
                # ניתוח הבעיה עם GPT
                gpt_result = analyze_problem(row["text_clean"])
                st.write("**GPT raw output:**", gpt_result)

                for line in gpt_result.split("\n"):
                    if "מוצר" in line and "|" in line:
                        try:
                            parts = line.split("|")
                            product_name = parts[0].split(":")[1].strip()
                            score = parts[1].split(":")[1].replace("%", "").strip()
                        except Exception as e:
                            st.write(f"Parsing error: {e}")
                            continue

                        # חיפוש לינק באליאקספרס
                        link = search_aliexpress(product_name)
                        st.write(f"Searching link for: {product_name} -> {link}")
                        results.append({
                            "problem": row["title"],
                            "product": product_name,
                            "match_percent": score,
                            "aliexpress_link": link if link else "לא נמצא קישור"
                        })

            if not results:
                st.warning("לא התקבלו מוצרים מ-GPT או שלא נמצאו קישורים.")
            else:
                output_df = pd.DataFrame(results)
                st.write("### תוצאות:")
                st.dataframe(output_df)
                st.download_button("Download CSV", output_df.to_csv(index=False), "output.csv")
