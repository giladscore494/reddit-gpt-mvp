from daily_trends import get_combined_trends
from analyze_gpt import analyze_problem
import pandas as pd

def run(domain="טכנולוגיה"):
    trends_df = get_combined_trends(domain)
    results = []
    for _, row in trends_df.iterrows():
        product, link = analyze_problem(row["topic"])
        results.append({
            "בעיה": row["topic"],
            "כמות פוסטים": row["posts_count"],
            "דרגת חום": row["heat"],
            "מוצר מוצע": product,
            "קישור": link
        })
    df = pd.DataFrame(results)
    print(df)
    df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    run()
