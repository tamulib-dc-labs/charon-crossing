import csv
from collections import defaultdict
import yaml
import os

INPUT_CSV = os.path.join(os.path.dirname(__file__), '..', 'charon_crossing', 'data', 'fedora_fields_generator.csv')
OUTPUT_YAML = os.path.join(os.path.dirname(__file__), '..', 'charon_crossing', 'data', 'fields_by_collection.yaml')


def main():
    field_collections = defaultdict(list)

    with open(INPUT_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            field_name = row['field_name'].strip()
            collection = row['collection'].strip()
            if field_name and collection:
                field_collections[field_name].append(collection)

    data = {field: {'collections': collections} for field, collections in sorted(field_collections.items())}

    with open(OUTPUT_YAML, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=True)

    print(f"Written to {OUTPUT_YAML}")


if __name__ == '__main__':
    main()
