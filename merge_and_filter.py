import pandas as pd

def merge_and_filter(dfs):
    """
    מאחד מספר DataFrames (Google News, Quora, StackExchange וכו'),
    מסיר כפילויות ומוסיף מדדים בסיסיים.
    """
    # ניקוי רשימות ריקות
    dfs = [df for df in dfs if df is not None and not df.empty]
    if not dfs:
        return pd.DataFrame()

    # איחוד
    df = pd.concat(dfs, ignore_index=True)

    # יצירת שדה טקסט לניקוי כפילויות
    df["text_clean"] = df.get("title", "").fillna("") + " " + df.get("snippet", "").fillna("")
    df = df.drop_duplicates(subset="text_clean")

    # הוספת מדד פופולריות בסיסי
    if "score" in df.columns:
        df["engagement_score"] = df["score"].fillna(0)
    else:
        df["engagement_score"] = 0

    # תדירות הופעה
    freq = df["text_clean"].value_counts().to_dict()
    df["frequency_score"] = df["text_clean"].apply(lambda x: freq.get(x, 1))

    return df
