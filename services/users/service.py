import bcrypt
from pydantic import EmailStr
from sqlalchemy import orm

from models import user

from . import exceptions, schema


class Service:
    def __init__(self, session: orm.Session):
        """Build User Service"""
        self.db = session

    def create_user(self, inp: schema.CreateUserSchema) -> schema.User:
        """Hash password and create user"""
        salt = bcrypt.gensalt()
        password = inp.password.encode()
        hashed_password = bcrypt.hashpw(password, salt)
        user_data = inp.dict()
        del user_data["password"]
        db_user = user.User(
            **user_data, hashed_password=hashed_password.decode()
        )  # noqa: E501
        self.db.add(instance=db_user)
        self.db.commit()
        self.db.refresh(db_user)
        user_schema = schema.User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_admin=db_user.is_admin,
        )
        return user_schema

    def get_user_by_id(self, id: int) -> schema.User:
        """Get user from id"""
        db_user = self.db.get(user.User, id)
        if db_user is None:
            raise exceptions.UserNotFoundException()
        user_schema = schema.User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_admin=db_user.is_admin,
        )
        return user_schema

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
