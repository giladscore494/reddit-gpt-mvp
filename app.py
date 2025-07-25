# app.py
import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from analyze_gpt import analyze_problem

st.title("Reddit GPT MVP - בעיות ופתרונות")

# בחירת נושא
topic = st.text_input("הזן נושא לחיפוש:", "dropshipping")

if topic:
    # שליפת פוסטים מרדיט
    with st.spinner("טוען פוסטים מרדיט..."):
        reddit_df = fetch_reddit_posts([topic], days=7)

    if not reddit_df.empty:
        st.subheader("פוסטים שנמצאו:")
        st.dataframe(reddit_df)

        # ניתוח הבעיות והצעת פתרון
        st.subheader("ניתוח בעיות והצעת פתרונות")
        products, links = [], []
        for _, row in reddit_df.iterrows():
            product, link = analyze_problem(row.title)
            products.append(product)
            links.append(link)

        reddit_df["מוצר מומלץ"] = products
        reddit_df["קישור"] = links

        st.dataframe(reddit_df)
    else:
        st.warning("לא נמצאו פוסטים לנושא זה.")
