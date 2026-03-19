import pandas as pd
import os


def transform_data(df):
    for col in df.columns:
        if col != "Image" and df[col].astype(str).str.contains(r'\|').any():
            df[col] = df[col].apply(
                lambda x: [s.strip() for s in str(x).split('|')] if '|' in str(x) else x
            )
    return df

files = []
for f in os.listdir("ami_output"):
    if f.endswith(".csv"):
        files.append(os.path.join("ami_output", f))

for file in files:
    df = pd.read_csv(file)
    df = transform_data(df)

    df.to_csv(file, index=False)

