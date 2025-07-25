import pandas as pd

def merge_and_filter(dfs):
    """
    מאחד את כל מקורות המידע, מסנן כפילויות, מוסיף ספירת הופעות לכל בעיה.
    """
    # איחוד כל המסגרות
    df = pd.concat([d for d in dfs if not d.empty], ignore_index=True)

    # אם אין נתונים
    if df.empty:
        return df

    # איחוד טקסט
    df["text_clean"] = df["title"].fillna("") + " " + df["text"].fillna("")

    # ספירה כמה פעמים הופיעה כל בעיה (title)
    freq = df.groupby("title").size().reset_index(name="post_count")

    # מיזוג חזרה
    df = df.merge(freq, on="title", how="left")

    # שמירת עמודות נדרשות בלבד
    df = df[["title", "text", "url", "source", "post_count"]].drop_duplicates()

    return df
