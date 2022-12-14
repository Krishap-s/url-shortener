from cassandra import cluster
from cassandra.auth import PlainTextAuthProvider

from settings import settings

db = None


def get_cassandra_db():
    global db
    if db is None:
        if settings.cassandra_username and settings.cassandra_password:
            auth_provider = PlainTextAuthProvider(
                username=settings.cassandra_username,
                password=settings.cassandra_password,
            )
            clstr = cluster.Cluster(
                [settings.cassandra_host], auth_provider=auth_provider
            )
        else:
            clstr = cluster.Cluster([settings.cassandra_host])
        db = clstr.connect(settings.cassandra_keyspace)
    return db
