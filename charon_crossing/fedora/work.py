from .object import FedoraObject
from .proxy import FedoraProxy
from .file import FedoraFile
from rdflib import URIRef, Graph


class FedoraWork(FedoraObject):
    def __init__(self, uri):
        super().__init__(uri)
        self.uri = URIRef(uri)
        self.descriptive_metadata = self.__get_descriptive_metadata()
        self._cache = {}
        self.iana_first = self.__get_iana('first')
        self.iana_last = self.__get_iana('last')

    def __get_iana(self, name):
        return next(self.content.objects(subject=self.uri, predicate=URIRef(f"{self.namespaces.iana}{name}")), None)

    def __get_descriptive_metadata(self):
        """Builds a graph with just known descriptive metadata."""
        description = Graph()
        descriptive_predicates = {
            f"{self.namespaces.dc}subject",
            f"{self.namespaces.dc}creator",
            f"{self.namespaces.dc}description",
            f"{self.namespaces.dc}format",
            f"{self.namespaces.dc}language",
            f"{self.namespaces.dc}publisher",
            f"{self.namespaces.dc}title",
            f"{self.namespaces.dc}type",
            f"{self.namespaces.dc}rights",
            f"{self.namespaces.dcterms}alternative",
            f"{self.namespaces.dcterms}created",
            f"{self.namespaces.dcterms}extent",
            f"{self.namespaces.dcterms}isPartOf",
            f"{self.namespaces.dcterms}medium",
            f"{self.namespaces.dcterms}spatial",
        }
        for s, p, o in self.content:
            if str(p) in descriptive_predicates:
                description.add((s, p, o))
        return description

    def __get_cached(self, key, func):
        """Helper to cache expensive operations."""
        if key not in self._cache:
            self._cache[key] = func()
        return self._cache[key]

    @property
    def rights(self):
        return self.__get_cached('rights', lambda: self.__get_first_literal(f"{self.namespaces.dc}rights"))

    @property
    def title(self):
        return self.__get_cached('title', lambda: self.__get_all_literals(f"{self.namespaces.dc}title"))

    @property
    def summary(self):
        return self.__get_cached('summary', lambda: self.__get_first_literal(f"{self.namespaces.dc}description"))

    @property
    def members(self):
        return self.__get_cached('members', lambda: self.__get_all_objects(f"{self.namespaces.pcdm}hasMember"))

    def __get_first_literal(self, predicate):
        for _, p, o in self.content:
            if str(p) == predicate:
                return str(o)
        return ""

    def __get_all_literals(self, predicate):
        return [str(o) for _, p, o in self.content if str(p) == predicate]

    def __get_all_objects(self, predicate):
        return [str(o) for _, p, o in self.content if str(p) == predicate]

    def get_ordered_members(self):
        ordered_members = []
        current = FedoraProxy(uri=str(self.iana_first))
        while current:
            ordered_members.append(current.get_proxy_for())
            if current.has_iana_next:
                current = FedoraProxy(uri=str(current.get_next()))
            else:
                current = None
        return ordered_members

    def get_ordered_member_files(self):
        ordered_members = []
        current = FedoraProxy(uri=str(self.iana_first))
        while current:
            current_part = FedoraFile(uri=str(current.get_proxy_for()))
            current_part_files = current_part.get_files()
            for current_file in current_part_files:
                ordered_members.append(str(current_file))
            if current.has_iana_next:
                current = FedoraProxy(uri=str(current.get_next()))
            else:
                current = None
        return ordered_members

    def get_members(self):
        return list(self.content.objects(
            subject=URIRef(self.uri), predicate=URIRef(f"{self.namespaces.pcdm}hasMember")
        ))

    def metadata_to_dict(self):
        predicates_map = {
            f"{self.namespaces.dcterms}alternative": "dcterms_alternative",
            f"{self.namespaces.dcterms}created": "dcterms_created",
            f"{self.namespaces.dcterms}issued": "dcterms_issued",
            f"{self.namespaces.dc}date": "dc_date",
            f"{self.namespaces.dc}subject": "dc_subject",
            f"{self.namespaces.dcterms}coverage": "dcterms_coverage",
            f"{self.namespaces.dcterms}temporal": "dcterms_temporal",
            f"{self.namespaces.dcterms}spatial": "dcterms_spatial",
            f"{self.namespaces.dc}creator": "dc_creator",
            f"{self.namespaces.dc}contributor": "dc_contributor",
            f"{self.namespaces.dc}publisher": "dc_publisher",
            f"{self.namespaces.dc}format": "dc_format",
            f"{self.namespaces.dc}type": "dc_type",
            f"{self.namespaces.dcterms}type": "dcterms_type",
            f"{self.namespaces.dcterms}medium": "dcterms_medium",
            f"{self.namespaces.dcterms}abstract": "dcterms_abstract",
            f"{self.namespaces.dc}abstract": "dc_abstract",
            f"{self.namespaces.dc}summary": "dc_summary",
            f"{self.namespaces.dc}description": "dc_description",
            f"{self.namespaces.dc}language": "dc_language",
            f"{self.namespaces.dcterms}extent": "dcterms_extent",
            f"{self.namespaces.dc}identifier": "dc_identifier",
            f"{self.namespaces.dcterms}otherIdentifier": "dcterms_otherIdentifier",
            f"{self.namespaces.dcterms}URL": "dcterms_URL",
            f"{self.namespaces.dc}rights": "dc_rights",
            f"{self.namespaces.dcterms}rightsHolder": "dcterms_rightsHolder",
            f"{self.namespaces.dcterms}rightsURI": "dcterms_rightsURI",
            f"{self.namespaces.dcterms}accessRights": "dcterms_accessRights",
            f"{self.namespaces.dcterms}isPartOf": "dcterms_isPartOf",
            f"{self.namespaces.dcterms}isPartOfSeries": "dcterms_isPartOfSeries",
            f"{self.namespaces.dcterms}lcc": "dcterms_lcc",
            f"{self.namespaces.dc}citation": "dc_citation",
            f"{self.namespaces.dc}genre": "dc_genre",
        }
        description = {label: [] for label in predicates_map.values()}
        for _, p, o in self.descriptive_metadata:
            label = predicates_map.get(str(p))
            if label:
                description[label].append(str(o))
        return description


if __name__ == '__main__':
    x = FedoraWork(
        'https://api.library.tamu.edu/fcrepo/rest/3b/6f/c3/25/3b6fc325-f6ca-41d8-b91e-8c5db3be8c13/london-collection_objects/9'
    )

