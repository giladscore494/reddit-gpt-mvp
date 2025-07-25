import pandas as pd

def merge_and_filter(dfs):
    # איחוד מסגרות נתונים
    dfs = [df for df in dfs if df is not None and not df.empty]
    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)

    # מניעת כפילויות
    df["text_clean"] = df["title"].fillna("") + " " + df["text"].fillna("")
    df = df.drop_duplicates(subset="text_clean")

    # חישוב מדדים
    if "score" in df.columns:
        df["engagement_score"] = df["score"].fillna(0)
    else:
        df["engagement_score"] = 0

    freq = df["text_clean"].value_counts().to_dict()
    df["frequency_score"] = df["text_clean"].apply(lambda x: freq.get(x, 1))

    return df
