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
    status: str = sqlalchemy.Enum("VALID", "INVALID", "PENDING", name="status")
    is_active: bool = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    link = orm.relationship("Link")
