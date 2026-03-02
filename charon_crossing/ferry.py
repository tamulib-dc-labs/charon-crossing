import click
from . import FedoraWork
from .fedora import FedoraCollection
from csv import DictWriter
from tqdm import tqdm


@click.command()
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


if __name__ == "__main__":
    ferry()
