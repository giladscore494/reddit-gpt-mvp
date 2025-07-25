import pandas as pd

def merge_and_filter(dfs):
    """
    מאחד מספר DataFrames (או DataFrame יחיד) ומסנן כפילויות על בסיס הטקסט הנקי.
    """
    # תומך במקרה שהקלט הוא DataFrame בודד
    if isinstance(dfs, pd.DataFrame):
        dfs = [dfs]

    # איחוד כל הנתונים
    df = pd.concat(dfs, ignore_index=True)

    # אם העמודה text_clean לא קיימת – נשתמש ב-title במקום
    if "text_clean" not in df.columns:
        df["text_clean"] = df["title"].fillna("")

    # הסרת כפילויות ושמירה על מקור, טקסט וכו'
    grouped = df.groupby("text_clean").agg({
        "source": lambda x: list(set(x)),
        "title": "first",
        "url": "first"
    }).reset_index()

    return grouped
