import pandas as pd

def save_to_csv(df, filename="output.csv"):
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}")
