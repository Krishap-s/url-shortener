import sqlalchemy
from sqlalchemy import orm

from infrastructure import db


class Link(db.Base):
    __tablename__ = "links"

    id: int = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True
    )  # noqa:E501
    key: str = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    reference: str = sqlalchemy.Column(sqlalchemy.String)
    owner_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    action: str = sqlalchemy.Column(
        sqlalchemy.Enum("REDIRECT", "WARN", "BLOCK", name="action")
    )
    is_active: bool = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    owner = orm.relationship("User")
