from cassandra import cluster

from settings import settings

clstr = cluster.Cluster()
session = clstr.connect(settings.cassandra_keyspace)
