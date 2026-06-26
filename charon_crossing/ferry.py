import click
from . import FedoraWork
from .fedora import FedoraCollection
from .iabookreader import IABookReaderMetadata
from csv import DictWriter
from tqdm import tqdm
import os


@click.group()
def cli():
    pass


@cli.command()
@click.argument("uri")
def ferry(uri):
    collection = FedoraCollection(uri)
    members = collection.get_contains()
    print(members)

    rows = []
    for member in tqdm(members):
        work = FedoraWork(member)
        row = {k: "|".join(v) for k, v in work.metadata_to_dict().items()}
        row["files"] = "|".join(work.get_ordered_member_files())
        rows.append(row)

    fieldnames = list(dict.fromkeys(k for row in rows for k in row))
    with open(f"{collection.uri.split('/')[-1]}.csv", "w", newline="", encoding="utf-8") as f:
        writer = DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


@cli.command()
@click.argument("uri")
def get_members(uri):
    all_collections = []
    collection = FedoraCollection(uri)
    for member in tqdm(collection.get_contains()):
        if "_objects" not in member:
            current = FedoraCollection(member)
            all_collections.append(
                {
                    "uri": str(member),
                    "created": str(current.get_created()),
                    "works": len(current.get_members()),
                }
            )
    with open("collections.csv", "w", newline="", encoding="utf-8") as f:
        writer = DictWriter(f, fieldnames=list(all_collections[0].keys()))
        writer.writeheader()
        writer.writerows(all_collections)


@cli.command()
@click.argument("path")
def ia_reader_metadata(path):
    all_metadata = []
    for path, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xml"):
                reader = IABookReaderMetadata(os.path.join(path, file))
                all_metadata.append(reader.build())
    with open("all_metadata.csv", "w", newline="", encoding="utf-8") as mycsv:
        writer = DictWriter(mycsv, fieldnames=list(all_metadata[0].keys()))
        writer.writeheader()
        writer.writerows(all_metadata)


if __name__ == "__main__":
    cli()
