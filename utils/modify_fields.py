import json
import os
import uuid

import pandas as pd

MEDIA_COLUMNS = {"Image", "Audio", "Video", "Document", "Transcript", "Captions"}


def safe_json(obj) -> str:
    """Serialize to JSON without \" sequences that confuse PHP's fgetcsv."""
    return json.dumps(obj).replace('\\"', '\\u0022')


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Generate a unique node_uuid for every row
    if "node_uuid" not in df.columns:
        df.insert(0, "node_uuid", [str(uuid.uuid4()) for _ in range(len(df))])

    for col in df.columns:
        if col == "node_uuid":
            continue

        if col in MEDIA_COLUMNS:
            # File columns: convert pipe separators to semicolons
            df[col] = df[col].apply(
                lambda x: str(x).replace("|", ";") if pd.notna(x) and "|" in str(x) else x
            )
        elif df[col].astype(str).str.contains(r"\|").any():
            # Multi-value fields: serialize as safe JSON array
            df[col] = df[col].apply(
                lambda x: safe_json([s.strip() for s in str(x).split("|")])
                if pd.notna(x) and "|" in str(x)
                else x
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
