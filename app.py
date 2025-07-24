import streamlit as st
import pandas as pd
from fetch_reddit import fetch_reddit_posts
from fetch_twitter import fetch_twitter
from fetch_google_trends import fetch_google_trends
from fetch_websearch import fetch_websearch
from merge_and_filter import merge_and_filter
from analyze_gpt import analyze_problem
from calc_roi import calculate_roi

st.title("Multi-Source Problem Finder → Product Ideas")

if st.button("Collect & Analyze"):
    reddit_df = fetch_reddit_posts(["BuyItForLife","LifeProTips"], days=7)
    twitter_df = fetch_twitter("problem", days=7)
    trends_df = fetch_google_trends()
    tiktok_df = fetch_websearch("problem", site="tiktok.com")
    quora_df = fetch_websearch("problem", site="quora.com")

    combined = merge_and_filter([reddit_df, twitter_df, trends_df, tiktok_df, quora_df])
    results = []
    for _, row in combined.iterrows():
        solution = analyze_problem(row["text_clean"])
        sell_price, roi = calculate_roi(10)
        results.append({
            "problem": row["title"],
            "sources": ", ".join(row["source"]),
            "products_solutions": solution,
            "cost_price": 10,
            "sell_price": sell_price,
            "roi_percent": roi
        })
    output_df = pd.DataFrame(results)
    st.write(output_df)
    st.download_button("Download CSV", output_df.to_csv(index=False), "output.csv")
