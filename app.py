import streamlit as st
from analyze_gpt import analyze_problem
from fetch_google_link import search_aliexpress
from trend_check import get_trend_score

st.title("Multi-Source Problem Finder → Product Ideas (AliExpress + Trend Check)")

topic = st.text_input("מה הבעיה או התחום שתרצה לחפש?")

def format_results(items, solution):
    html = f"<h3>פתרון מהשורש:</h3><p>{solution}</p><h3>מוצרים מומלצים:</h3>"
    for item in items:
        html += f"""
        <div style="margin-bottom:20px; padding:10px; border:1px solid #ddd; border-radius:8px;">
            <b>{item['name']}</b> – התאמה {item['match']}% ({item['trend']})<br>
            <span style="color:gray;font-size:14px">{item['explanation']}</span><br>
            <a href="{item['link']}" target="_blank"
               style="color:white;background:#0073e6;padding:5px 10px;
               border-radius:5px;text-decoration:none;display:inline-block;margin-top:5px;">
               🔗 לחץ כאן
            </a>
        </div>
        """
    return html

if st.button("Analyze Problem") and topic:
    with st.spinner("מחפש ומנתח פתרונות..."):
        analysis = analyze_problem(topic)
        solution = analysis.get("solution", "לא נמצאה תשובה.")
        products = analysis.get("products", [])

        result_list = []
        for p in products:
            name = p["product"]
            trend = get_trend_score(name)
            link = search_aliexpress(name)
            result_list.append({
                "name": name,
                "match": p["match"],
                "explanation": p["explanation"],
                "link": link,
                "trend": trend
            })

        st.markdown(format_results(result_list, solution), unsafe_allow_html=True)
