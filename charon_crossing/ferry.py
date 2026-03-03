import click
from . import FedoraWork
from .fedora import FedoraCollection
from csv import DictWriter
from tqdm import tqdm


@click.group()
def cli():
    pass


@cli.command()
@click.argument("uri")
def ferry(uri):
    collection = FedoraCollection(uri)
    members = collection.get_members()

    rows = []
    for member in tqdm(members):
        work = FedoraWork(member)
        row = {k: "|".join(v) for k, v in work.metadata_to_dict().items()}
        row["files"] = "|".join(work.get_ordered_member_files())
        rows.append(row)

    with open(f"{collection.uri.split('/')[-1]}.csv", "w", newline="") as f:
        writer = DictWriter(f, fieldnames=list(rows[0].keys()))
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
    with open("collections.csv", "w", newline="") as f:
        writer = DictWriter(f, fieldnames=list(all_collections[0].keys()))
        writer.writeheader()
        writer.writerows(all_collections)


if __name__ == "__main__":
    cli()
