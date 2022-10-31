from cassandra import cluster
from cassandra.auth import PlainTextAuthProvider

from settings import settings

db = None


def get_cassandra_db():
    global db
    if db is None:
        auth = PlainTextAuthProvider(
            username=settings.cassandra_username,
            password=settings.cassandra_password,  # noqa: E501
        )
        clstr = cluster.Cluster([settings.cassandra_host], auth_provider=auth)
        db = clstr.connect(settings.cassandra_keyspace)
    return db
