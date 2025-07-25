import streamlit as st
from analyze_gpt import analyze_problem
from fetch_google_link import search_aliexpress
from trend_check import get_trend_score
from daily_trends import fetch_daily_trends

st.title("Multi-Source Problem Finder → Product Ideas (AliExpress + Trend Check + Daily Top 10)")

topic = st.text_input("מה הבעיה או התחום שתרצה לחפש?")

def format_products(products):
    html = "<h3>מוצרים מומלצים:</h3>"
    for item in products:
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

def format_daily_trends(trends):
    html = "<h3>טופ 10 מוצרים פופולריים היום (Google Trends):</h3>"
    for t in trends:
        link = search_aliexpress(t)
        html += f"""
        <div style="margin-bottom:10px;">
            <b>{t}</b><br>
            <a href="{link}" target="_blank"
               style="color:white;background:#0073e6;padding:3px 7px;
               border-radius:5px;text-decoration:none;display:inline-block;margin-top:2px;">
               🔗 לחץ כאן
            </a>
        </div>
        """
    return html

if st.button("Analyze Problem") and topic:
    with st.spinner("מחפש ומנתח פתרונות..."):
        analysis = analyze_problem(topic)
        problems = analysis.get("problems", [])
        products = analysis.get("products", [])

        # הוספת לינקים וטרנדיות למוצרים
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

        # טופ 10 יומיים
        daily_products = fetch_daily_trends()

        st.markdown(f"<h3>בעיות חוזרות שזוהו:</h3><ul>{''.join([f'<li>{x}</li>' for x in problems])}</ul>", unsafe_allow_html=True)
        st.markdown(format_products(result_list), unsafe_allow_html=True)
        st.markdown(format_daily_trends(daily_products), unsafe_allow_html=True)
