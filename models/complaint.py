import sqlalchemy
from sqlalchemy import orm

from infrastructure import db


class Complaint(db.Base):
    __tablename__ = "complaints"

    id: int = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, index=True
    )  # noqa:E501
    link_id: int = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("links.id")
    )
    body: str = sqlalchemy.Column(sqlalchemy.String(1000))
    status: str = sqlalchemy.Column(
        sqlalchemy.Enum("VALID", "INVALID", "PENDING", name="status")
    )

    link = orm.relationship("Link")
