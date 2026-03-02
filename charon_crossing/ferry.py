from . import FedoraWork
from .fedora import FedoraCollection
from csv import DictWriter

collection = FedoraCollection('https://api-pre.library.tamu.edu/fcrepo/rest/london-maps-spotlight-example')
members = collection.get_members()

rows = []
for member in members:
    work = FedoraWork(member)
    row = {k: "|".join(v) for k, v in work.metadata_to_dict().items()}
    row["files"] = "|".join(work.get_ordered_member_files())
    rows.append(row)

with open(f"{collection.uri.split('/')[-1]}.csv", "w", newline="") as f:
    writer = DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
