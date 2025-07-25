import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from analyze_gpt import analyze_problem

st.title("Top 3 Hot Problems → AliExpress Solutions")
st.write("כתבו תחום כללי (לדוגמה: אופנה, ספורט, טכנולוגיה)")

topic = st.text_input("נושא כללי")

if st.button("חפש"):
    if not topic.strip():
        st.warning("אנא הזינו תחום לחיפוש.")
    else:
        st.info(f"מחפש בעיות עם מילת מפתח: **{topic}** ...")
        
        # --- שלב 1: איסוף פוסטים מ-Reddit ---
        reddit_df = fetch_reddit_posts([topic], days=7)
        
        if reddit_df.empty:
            st.warning("לא נמצאו פוסטים רלוונטיים לנושא זה.")
        else:
            st.success(f"נמצאו {len(reddit_df)} פוסטים לניתוח.")
            
            # --- שלב 2: ניתוח 3 בעיות חמות ---
            hot_problems = reddit_df.head(3)  # כרגע פשוט לוקחים את הראשונות
            
            results = []
            for _, row in hot_problems.iterrows():
                problem_text = row.title
                product, link = analyze_problem(problem_text)
                
                # הוספת תוצאה לטבלה
                results.append({
                    "problem": problem_text,
                    "product": product,
                    "link": link
                })
            
            # --- שלב 3: הצגת פלט ---
            st.subheader("3 בעיות חמות והמוצרים שמומלץ למכור:")
            for idx, item in enumerate(results, start=1):
                st.write(f"**{idx}. {item['problem']}**")
                st.write(f"מוצר מוצע: **{item['product']}**")
                st.markdown(f"[🔗 לחץ כאן כדי לראות]({item['link']})")

            st.markdown("---")
            st.caption("💡 מבוסס על טרנדים אחרונים + ניתוח GPT לאנלוגיות בעיות → פתרונות")
