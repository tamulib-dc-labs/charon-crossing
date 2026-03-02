from .object import FedoraObject
from rdflib import URIRef, Graph


class FedoraCollection(FedoraObject):
    def __init__(self, uri):
        super().__init__(uri)
        self.uri = URIRef(uri)
        self._cache = {}

    def get_members(self):
        return list(self.content.objects(
            subject=URIRef(self.uri), predicate=URIRef(f"{self.namespaces.pcdm}hasMember")
        ))

    def get_contains(self):
        return list(self.content.objects(
            subject=URIRef(self.uri), predicate=URIRef(f"{self.namespaces.ldp}contains")
        ))

    def get_created(self):
        return next(self.content.objects(subject=self.uri, predicate=URIRef(f"{self.namespaces.fedora}created")), None)


if __name__ == '__main__':
    x = FedoraCollection(
        'https://api.library.tamu.edu/fcrepo/rest/a6/f0/55/01/a6f05501-9312-4fd5-a167-f7ce2fa28ca6'
    )
    print(x.get_members())