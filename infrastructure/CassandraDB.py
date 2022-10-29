from cassandra import cluster

from settings import settings

db = None


def get_cassandra_db():
    global db
    if db is None:
        clstr = cluster.Cluster(
            [settings.cassandra_host],
        )
        db = clstr.connect(settings.cassandra_keyspace)
    return db
