from .fedora import FedoraCollection
x = FedoraCollection('https://api-pre.library.tamu.edu/fcrepo/rest/bb/97/f2/3e/bb97f23e-803a-4bd6-8406-06802623554c')
print(x.get_members())