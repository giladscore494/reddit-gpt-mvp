from fetch_reddit import fetch_reddit_posts
from analyze_gpt import analyze_post
from calc_roi import calculate_roi
from save_to_csv import save_to_csv
import pandas as pd

def main():
    subreddits = ["fashion", "SkincareAddiction"]
    df = fetch_reddit_posts(subreddits)

    analyses = []
    for _, row in df.iterrows():
        analysis = analyze_post(row["title"], row["text"])
        sell_price, roi = calculate_roi(10)  # מחיר עלות לדוגמה
        analyses.append({
            "title": row["title"],
            "problem_solutions": analysis,
            "cost_price": 10,
            "sell_price": sell_price,
            "roi_percent": roi
        })

    output_df = pd.DataFrame(analyses)
    save_to_csv(output_df)

if __name__ == "__main__":
    main()
