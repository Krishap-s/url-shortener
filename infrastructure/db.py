import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.ext import declarative

from settings import settings

engine = sqlalchemy.create_engine(
    settings.database_url.replace("postgres://", "postgresql://"), echo=True
)

SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative.declarative_base()
