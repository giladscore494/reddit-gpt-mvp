from daily_trends import get_combined_trends
from analyze_gpt import analyze_problem
import pandas as pd

def run(domain="טכנולוגיה"):
    # קבלת טרנדים
    trends_df = get_combined_trends(domain)

    # סינון ל-3 בעיות הכי חמות
    top_trends = trends_df.sort_values(by="posts_count", ascending=False).head(3).reset_index(drop=True)

    results = []
    for _, row in top_trends.iterrows():
        product, link = analyze_problem(row["topic"])
        results.append({
            "בעיה": row["topic"],
            "כמות פוסטים": row["posts_count"],
            "דרגת חום": row["heat"],
            "מוצר מוצע": product,
            "קישור למוצר": link
        })

    df = pd.DataFrame(results)
    print(df)
    df.to_csv("results.csv", index=False)

if __name__ == "__main__":
    run()
