import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from analyze_gpt import analyze_post
from calc_roi import calculate_roi

st.title("Reddit → GPT → Product Ideas (Dropshipping)")

subreddit = st.text_input("Enter Subreddit", "AskReddit")

if st.button("Run Analysis"):
    df = fetch_reddit_posts([subreddit])
    results = []
    for _, row in df.iterrows():
        analysis = analyze_post(row["title"], row["text"])
        sell_price, roi = calculate_roi(10)
        results.append({
            "title": row["title"],
            "products_solutions": analysis,
            "cost_price": 10,
            "sell_price": sell_price,
            "roi_percent": roi
        })
    output_df = pd.DataFrame(results)
    st.write(output_df)
    st.download_button("Download CSV", output_df.to_csv(index=False), "output.csv")
