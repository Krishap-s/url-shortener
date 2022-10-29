import random
import string

from sqlalchemy import orm

from models import link

from . import exceptions, schema


class Service:
    def __init__(self, session: orm.Session, cassandra_session):
        """Build Link Service"""
        self.cassandra_session = cassandra_session
        self.db = session

    def create_link(
        self, inp: schema.CreateLinkSchema, owner_id: int
    ) -> schema.Link:  # noqa: E501
        """Create new link"""
        letters = string.ascii_lowercase
        key = "".join(random.choice(letters) for i in range(10))
        stmt = self.cassandra_session.prepare(
            "INSERT INTO urls (key, reference, action, owner_id, is_active) VALUES (?,?,?,?,?);"  # noqa: E501
        )
        db_link = link.Link(
            **inp.dict(), key=key, owner_id=owner_id, action="REDIRECT"
        )  # noqa: E501
        self.db.add(db_link)
        self.db.commit()
        self.db.refresh(db_link)
        self.cassandra_session.execute(
            stmt, (key, inp.reference, "REDIRECT", owner_id, True)
        )
        res = schema.Link(
            id=db_link.id,
            key=db_link.key,
            reference=db_link.reference,
            owner_id=db_link.owner_id,
            action=db_link.action,
            is_active=db_link.is_active,
        )
        return res

    def get_link_by_key(self, key: str) -> schema.Link:
        """Get link from key"""
        stmt = self.cassandra_session.prepare(
            "SELECT * FROM urls WHERE key = ? ;"
        )  # noqa: E501
        rows = self.cassandra_session.execute(stmt, (key,))
        if rows.one() is None:
            raise exceptions.LinkNotFoundException()
        res = rows.one()
        res = schema.Link(
            key=res.key,
            reference=res.reference,
            action=res.action,
            owner_id=res.owner_id,
            is_active=res.is_active,
        )
        return res

    '''

    def get_user_by_username(self, username: str) -> schema.User:
        """Get user from username"""
        db_user = self.db.query(user.User).filter_by(username=username).first()
        if db_user is None:
            raise exceptions.UserNotFoundException()
        user_schema = schema.User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_admin=db_user.is_admin,
        )
        return user_schema

    def get_user_by_email(self, email: EmailStr) -> schema.User:
        """Get user from email"""
        db_user = self.db.query(user.User).filter_by(email=email).first()
        if db_user is None:
            raise exceptions.UserNotFoundException()
        user_schema = schema.User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_admin=db_user.is_admin,
        )
        return user_schema

    def authenticate(self, inp: schema.AuthenticateSchema) -> schema.User:
        """Validate if username and hashed password exists"""
        password = inp.password.encode()
        db_user = (
            self.db.query(user.User).filter_by(username=inp.username).first()
        )  # noqa:E501
        if db_user is None:
            raise exceptions.UserNotFoundException()
        if not bcrypt.checkpw(password, db_user.hashed_password.encode()):
            raise exceptions.InvalidCredentials()
        user_schema = schema.User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_admin=db_user.is_admin,
        )
        return user_schema
'''
