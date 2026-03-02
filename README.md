# charon-crossing

A Python library and CLI tool for migrating content from a Fedora repository into Archipelago. It traverses PCDM-structured collections, extracts descriptive metadata, and resolves ordered file members.

## Installation

```bash
poetry install
```

## CLI Usage

The `ferry` command takes a Fedora collection URI and writes a CSV of descriptive metadata and ordered file members to the current directory. The output file is named after the last path segment of the URI.

```bash
ferry <collection-uri>
```

**Example:**

```bash
ferry https://api.library.tamu.edu/fcrepo/rest/3b/6f/c3/25/3b6fc325-f6ca-41d8-b91e-8c5db3be8c13/graydiary-saf
```

This produces `graydiary-saf.csv` with one row per work and the following columns:

| Column | Source |
|---|---|
| `dcterms_alternative` | `dcterms:alternative` |
| `dcterms_datecreated` | `dcterms:created` |
| `dc_subject` | `dc:subject` |
| `dc_creator` | `dc:creator` |
| `dc_publisher` | `dc:publisher` |
| `dcterms_ispartof` | `dcterms:isPartOf` |
| `dc_format` | `dc:format` |
| `dc_type` | `dc:type` |
| `dcterms_medium` | `dcterms:medium` |
| `dc_description` | `dc:description` |
| `dc_language` | `dc:language` |
| `dcterms_extent` | `dcterms:extent` |
| `files` | Ordered file URIs via PCDM/IANA linked list |

Multi-valued fields are pipe-delimited (e.g. `History|Art`).

## Library Usage

The package exposes several classes for working with Fedora objects directly:

```python
from charon_crossing import FedoraCollection, FedoraWork, FedoraFile, FedoraProxy

# Retrieve a collection and its members
collection = FedoraCollection("https://...")
members = collection.get_members()

# Work with an individual work
work = FedoraWork(members[0])
print(work.title)
print(work.rights)
print(work.metadata_to_dict())
print(work.get_ordered_member_files())

# Access a file object
file = FedoraFile("https://.../fcrepo/rest/.../file")
file.download("/path/to/output")
```

### Classes

**`FedoraCollection(uri)`**
- `get_members()` — returns a list of member URIs via `pcdm:hasMember`
- `get_contains()` — returns a list of contained URIs via `ldp:contains`

**`FedoraWork(uri)`**
- `title` — list of `dc:title` values
- `rights` — first `dc:rights` value
- `summary` — first `dc:description` value
- `members` — list of `pcdm:hasMember` URIs
- `metadata_to_dict()` — dict of descriptive metadata with pipe-joined values ready for CSV export
- `get_ordered_members()` — members in order via IANA linked list
- `get_ordered_member_files()` — ordered list of file URIs

**`FedoraFile(uri)`**
- `get_files()` — returns `pcdm:hasFile` URIs
- `download(path)` — downloads the file to the given directory
- `get_cantaloupe_base_64()` — returns a IIIF `info.json` URL with base64-encoded identifier

**`FedoraProxy(uri)`**
- `get_proxy_for()` — returns the `ore:proxyFor` target URI
- `get_next()` — returns the next proxy in the IANA linked list
