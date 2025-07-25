import streamlit as st
import pandas as pd
from analyze_gpt import analyze_problem
from fetch_google_link import search_aliexpress

st.title("Multi-Source Problem Finder → Product Ideas (AliExpress Only)")

topic = st.text_input("מה הבעיה או התחום שתרצה לחפש?")
if st.button("Analyze Problem") and topic:
    with st.spinner("מחפש ומנתח פתרונות..."):
        analysis = analyze_problem(topic)
        solution = analysis.get("solution", "לא נמצאה תשובה.")
        products = analysis.get("products", [])

        # בניית טבלת מוצרים
        result_list = []
        for p in products:
            name = p["product"]
            link = search_aliexpress(name)
            result_list.append({
                "name": name,
                "match": p["match"],
                "explanation": p["explanation"],
                "link": link
            })

        # עיצוב פלט יפה
        def format_results(items):
            html = f"<h3>פתרון מהשורש:</h3><p>{solution}</p><h3>מוצרים מומלצים:</h3>"
            for item in items:
                html += f"""
                <div style="margin-bottom:20px">
                    <b>{item['name']}</b> – התאמה {item['match']}%<br>
                    <span style="color:gray;font-size:14px">{item['explanation']}</span><br>
                    <a href="{item['link']}" target="_blank"
                       style="color:white;background:#0073e6;padding:5px 10px;
                       border-radius:5px;text-decoration:none;display:inline-block;margin-top:5px;">
                       🔗 לחץ כאן
                    </a>
                </div>
                """
            return html

        st.markdown(format_results(result_list), unsafe_allow_html=True)
