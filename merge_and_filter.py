import pandas as pd

def merge_and_filter(dfs):
    """
    מאחד מספר DataFrames (או DataFrame יחיד) ומסנן כפילויות על בסיס הטקסט הנקי.
    אם חסרות עמודות מסוימות – יוסיף אותן כברירת מחדל.
    """
    # תומך בקלט של DataFrame יחיד
    if isinstance(dfs, pd.DataFrame):
        dfs = [dfs]

    # איחוד כל הנתונים
    df = pd.concat(dfs, ignore_index=True)

    # אם חסרה עמודת text_clean – ניצור אותה על בסיס title אם קיים
    if "text_clean" not in df.columns:
        if "title" in df.columns:
            df["text_clean"] = df["title"].fillna("")
        else:
            df["text_clean"] = ""

    # אם חסרה עמודת title – ניצור אותה ריקה
    if "title" not in df.columns:
        df["title"] = df["text_clean"]

    # אם חסרה עמודת url – נוסיף ריקה
    if "url" not in df.columns:
        df["url"] = ""

    # אם חסרה עמודת source – נוסיף ערך כללי
    if "source" not in df.columns:
        df["source"] = "unknown"

    # הסרת כפילויות
    grouped = df.groupby("text_clean").agg({
        "source": lambda x: list(set(x)),
        "title": "first",
        "url": "first"
    }).reset_index()

    return grouped
