# charon-crossing

A Python library and CLI tool for migrating content from a Fedora repository into Archipelago. It traverses PCDM-structured collections, extracts descriptive metadata, and resolves ordered file members.

## Installation

```bash
poetry install
```

## CLI Usage

The `ferry` CLI provides two subcommands. Run `ferry --help` to see all options.

---

### `ferry ferry` — Export collection works to CSV

Iterates the works in a Fedora collection and writes a CSV of descriptive metadata and ordered file URIs. The output file is named after the last path segment of the collection URI.

```bash
ferry ferry <collection-uri>
```

**Example:**

```bash
ferry ferry https://api.library.tamu.edu/fcrepo/rest/3b/6f/c3/25/3b6fc325-f6ca-41d8-b91e-8c5db3be8c13/graydiary-saf
```

Produces `graydiary-saf.csv` with one row per work. Multi-valued fields are pipe-delimited (e.g. `History|Art`).

| Column | Source |
|--------|--------|
| `dcterms_alternative` | `dcterms:alternative` |
| `dcterms_created` | `dcterms:created` |
| `dcterms_issued` | `dcterms:issued` |
| `dc_date` | `dc:date` |
| `dc_subject` | `dc:subject` |
| `dcterms_coverage` | `dcterms:coverage` |
| `dcterms_temporal` | `dcterms:temporal` |
| `dcterms_spatial` | `dcterms:spatial` |
| `dc_creator` | `dc:creator` |
| `dc_contributor` | `dc:contributor` |
| `dc_publisher` | `dc:publisher` |
| `dc_format` | `dc:format` |
| `dc_type` | `dc:type` |
| `dcterms_type` | `dcterms:type` |
| `dcterms_medium` | `dcterms:medium` |
| `dcterms_abstract` | `dcterms:abstract` |
| `dc_summary` | `dc:summary` |
| `dc_description` | `dc:description` |
| `dc_language` | `dc:language` |
| `dcterms_extent` | `dcterms:extent` |
| `dc_identifier` | `dc:identifier` |
| `dcterms_otherIdentifier` | `dcterms:otherIdentifier` |
| `dcterms_URL` | `dcterms:URL` |
| `dc_rights` | `dc:rights` |
| `dcterms_rightsHolder` | `dcterms:rightsHolder` |
| `dcterms_rightsURI` | `dcterms:rightsURI` |
| `dcterms_accessRights` | `dcterms:accessRights` |
| `dcterms_isPartOf` | `dcterms:isPartOf` |
| `dcterms_isPartOfSeries` | `dcterms:isPartOfSeries` |
| `dcterms_lcc` | `dcterms:lcc` |
| `dc_citation` | `dc:citation` |
| `dc_genre` | `dc:genre` |
| `files` | Ordered file URIs via PCDM/IANA linked list |

---

### `ferry get-members` — List sub-collections as CSV

Iterates the contents of a top-level Fedora container and writes a summary of each sub-collection to `collections.csv`.

```bash
ferry get-members <container-uri>
```

**Example:**

```bash
ferry get-members https://api.library.tamu.edu/fcrepo/rest/3b/6f/c3/25/3b6fc325-f6ca-41d8-b91e-8c5db3be8c13
```

Produces `collections.csv` with columns:

| Column | Description |
|--------|-------------|
| `uri` | Full URI of the sub-collection |
| `created` | Creation date of the sub-collection |
| `works` | Number of works (`pcdm:hasMember`) in the sub-collection |

---

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
