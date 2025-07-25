import streamlit as st
import pandas as pd
import re
from fetch_reddit import fetch_reddit_posts
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_problem
from fetch_google_link import search_aliexpress

# --- כותרת האפליקציה ---
st.title("Multi-Source Problem Finder → Product Ideas")

# --- קלט מהמשתמש ---
keyword = st.text_input("מה הבעיה או התחום שתרצה לחפש?", "")

# --- כפתור הפעלה ---
if st.button("Collect & Analyze"):
    if keyword.strip() == "":
        st.warning("אנא הזן מילה או תחום לחיפוש.")
    else:
        st.write(f"מחפש בעיות עם מילת מפתח: **{keyword}** ...")

        # --- שליפת נתונים ממקורות שונים ---
        reddit_df = fetch_reddit_posts(["BuyItForLife", "LifeProTips"], days=7)
        trends_df = fetch_google_trends()
        tiktok_df = fetch_websearch(keyword, site="tiktok.com")
        quora_df = fetch_websearch(keyword, site="quora.com")

        st.write(f"Reddit results: {len(reddit_df)}, Trends: {len(trends_df)}, TikTok: {len(tiktok_df)}, Quora: {len(quora_df)}")

        combined = merge_and_filter([reddit_df, trends_df, tiktok_df, quora_df])
        if combined.empty:
            st.warning("לא נמצאו בעיות עם מילת המפתח הזו.")
        else:
            # --- חיפוש בעיות שרלוונטיות למילת החיפוש (תמיכה בעברית) ---
            pattern = re.compile(re.escape(keyword), re.IGNORECASE)
            filtered = combined[combined["text_clean"].apply(lambda x: bool(pattern.search(str(x))))]

            if not filtered.empty:
                top_problem = filtered.iloc[0]["text_clean"]
            else:
                top_problem = keyword  # fallback – שולחים ישירות את מילת החיפוש ל-GPT

            st.write(f"### Top Problem Selected:\n{top_problem}")

            # --- קריאה ל-GPT ---
            gpt_result = analyze_problem(top_problem)
            st.write("**GPT raw output:**", gpt_result)

            # --- עיבוד תוצאות GPT ---
            results = []
            goal_line = None

            for line in gpt_result.split("\n"):
                if line.startswith("Goal:"):
                    goal_line = line.replace("Goal:", "").strip()
                if "Product" in line and "|" in line:
                    try:
                        product_name = line.split("|")[0].split(":")[1].strip()
                        score = line.split("|")[1].split(":")[1].replace("%", "").strip()
                    except Exception:
                        continue

                    # קישור חיפוש מדויק יותר (שם המוצר במלואו)
                    query = product_name.replace(" ", "+")
                    link = f"https://www.aliexpress.com/wholesale?SearchText={query}"

                    results.append({
                        "Product": f"**{product_name}**",
                        "Match": f"{score}%",
                        "Link": f"[🔗 View Product]({link})"
                    })

            # --- הצגת פלט ---
            if results:
                if goal_line:
                    st.write(f"### Goal identified by AI: {goal_line}")
                output_df = pd.DataFrame(results)
                st.write("### Recommended Products")
                st.write(output_df.to_html(escape=False, index=False), unsafe_allow_html=True)
                st.download_button("Download CSV", output_df.to_csv(index=False), "output.csv")
            else:
                st.warning("לא התקבלו מוצרים מתאימים.")
