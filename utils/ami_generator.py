import pandas as pd
import yaml
from pathlib import Path


def load_yaml(yaml_path):
    with open(yaml_path, "r") as f:
        return yaml.safe_load(f)


def build_mapping(yaml_data, collection):
    mapping = {}

    fields = yaml_data.get("fields", {})

    for arch_field, field_info in fields.items():
        collections = field_info.get("Collections", {})

        if collection in collections:
            fedora_fields = collections[collection]

            for fedora_field in fedora_fields:
                mapping[fedora_field] = arch_field

    return mapping


def transform_csv(csv_path, yaml_data, output_dir):

    collection = csv_path.stem
    mapping = build_mapping(yaml_data, collection)

    if not mapping:
        return "no_mapping", collection

    df = pd.read_csv(csv_path)

    cols = [c for c in df.columns if c in mapping]

    if not cols:
        return "no_columns", collection

    df_out = df[cols].rename(columns=mapping)

    output_file = output_dir / f"{collection}_ami.csv"
    df_out.to_csv(output_file, index=False)

    return "processed", collection


def generate_all(csv_folder, yaml_file, output_folder):

    csv_folder = Path(csv_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(exist_ok=True)

    yaml_data = load_yaml(yaml_file)

    processed = 0

    skipped_no_mapping = []
    skipped_no_columns = []

    for csv_file in csv_folder.glob("*.csv"):

        result, name = transform_csv(csv_file, yaml_data, output_folder)

        if result == "processed":
            processed += 1

        elif result == "no_mapping":
            skipped_no_mapping.append(name)

        elif result == "no_columns":
            skipped_no_columns.append(name)

    print(f"Processed files: {processed}")

    print(f"\nSkipped (no YAML mapping): {len(skipped_no_mapping)}")
    for f in skipped_no_mapping:
        print(f"  - {f}")

    print(f"\nSkipped (no matching columns): {len(skipped_no_columns)}")
    for f in skipped_no_columns:
        print(f"  - {f}")

    total_skipped = len(skipped_no_mapping) + len(skipped_no_columns)
    print(f"\nTotal skipped: {total_skipped}")


if __name__ == "__main__":

    YAML_FILE = "fedora.yml"
    CSV_FOLDER = "csv_data_files"
    OUTPUT_FOLDER = "ami_output"

    generate_all(CSV_FOLDER, YAML_FILE, OUTPUT_FOLDER)