import sqlalchemy
from settings import settings

engine = sqlalchemy.create_engine(settings.database_url)
