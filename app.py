import streamlit as st
from daily_trends import fetch_top3_products_by_topic

st.set_page_config(page_title="Top 3 Hot Problems → AliExpress Solutions", layout="centered")

st.title("Top 3 Hot Problems → AliExpress Solutions")

topic = st.text_input("כתבו תחום כללי (לדוגמה: אופנה, ספורט, טכנולוגיה)")

if st.button("חפש פתרונות"):
    results = fetch_top3_products_by_topic(topic)
    if not results:
        st.warning("לא נמצאו נושאים חמים השבוע בתחום הזה.")
    else:
        st.markdown("## 3 בעיות חמות והמוצרים שמומלץ למכור:")
        for idx, item in enumerate(results, start=1):
            st.markdown(f"""
            ### {idx}. {item['problem']}
            **מוצר מוצע:** {item['product']}  
            [🔗 לחץ כאן כדי לראות]({item['link']})
            """)

st.info("💡 מבוסס על טרנדים אחרונים + ניתוח GPT לאנלוגיות בעיות → פתרונות")
