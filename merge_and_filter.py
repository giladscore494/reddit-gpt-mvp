import pandas as pd

def merge_and_filter(dfs):
    # מיזוג כל הנתונים לרשימה אחת
    df = pd.concat(dfs, ignore_index=True)

    # הבטחת קיום עמודות source ו-url
    if "source" not in df.columns:
        df["source"] = "unknown"
    if "url" not in df.columns:
        df["url"] = df["text_clean"]

    # קיבוץ לפי טקסט כדי למנוע כפילויות
    grouped = df.groupby('text_clean').agg({
        'source': lambda x: list(set(x)),
        'title': 'first',
        'url': 'first'
    }).reset_index()

    return grouped
