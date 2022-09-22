import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from settings import settings

engine = sqlalchemy.create_engine(
    settings.database_url.replace("postgres://", "postgresql://"), echo=True
)

SessionLocal = orm.scoped_session(
    orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

db = None


def get_db():
    global db
    if db is not None:
        return db
    db = SessionLocal()
    return db


Base = declarative.declarative_base()
