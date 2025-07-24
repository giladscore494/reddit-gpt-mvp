import pandas as pd

def merge_and_filter(dfs):
    df = pd.concat(dfs, ignore_index=True)
    df['text_clean'] = df['text'].str.lower()
    # קיבוץ לפי בעיות דומות (פשטני)
    grouped = df.groupby('text_clean').agg({
        'source': lambda x: list(set(x)),
        'title': 'first',
        'url': 'first'
    }).reset_index()
    grouped['source_count'] = grouped['source'].apply(len)
    # רק בעיות שהופיעו ביותר ממקור אחד
    return grouped[grouped['source_count'] > 1]
