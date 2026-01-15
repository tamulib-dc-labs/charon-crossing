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


if __name__ == '__main__':
    x = FedoraCollection('https://api-pre.library.tamu.edu/fcrepo/rest/bb/97/f2/3e/bb97f23e-803a-4bd6-8406-06802623554c')
    print(x.get_members())