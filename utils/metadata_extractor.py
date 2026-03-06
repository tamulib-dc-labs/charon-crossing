import os
import pandas as pd

folder = "."
rows = []

for file in os.listdir(folder):

    if file.endswith(".csv"):

        path = os.path.join(folder, file)
        collection = file.replace(".csv", "")

        try:
            df = pd.read_csv(path, nrows=0)

            headers = df.columns.tolist()

            for field in headers:
                rows.append({
                    "field_name": field,
                    "collection": collection,
                    "csv_file": file
                })

        except pd.errors.EmptyDataError:
            print(f"Skipping empty file: {file}")

result = pd.DataFrame(rows)

result.to_csv("fedora_fields_generator.csv", index=False)

