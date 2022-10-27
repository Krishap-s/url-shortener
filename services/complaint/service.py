import typing

from sqlalchemy import orm

from models import complaint, link

from . import exceptions, schema


class Service:
    def __init__(self, session: orm.Session):
        """Build Complaint Service"""
        self.db = session

    def create_complaint(
        self, inp: schema.CreateComplaintSchema
    ) -> schema.Complaint:  # noqa: E501
        """Create new complaint using link key"""
        db_link = (
            self.db.query(link.Link)
            .filter(link.Link.key == inp.link_key)
            .first()  # noqa: E501
        )  # noqa: E501
        if db_link is None:
            raise exceptions.LinkNotFoundException()
        db_complaint = complaint.Complaint(
            body=inp.body, link_id=db_link.id, status="PENDING"
        )
        self.db.add(db_complaint)
        self.db.commit()
        self.db.refresh(db_complaint)
        res = schema.Complaint(
            id=db_complaint.id,
            body=db_complaint.body,
            status=db_complaint.status,
            link_id=db_complaint.link.id,
        )
        return res

    def get_complaints_by_link(
        self, link_key: str
    ) -> typing.List[schema.Complaint]:  # noqa: E501
        """Get complaint associated by link key"""
        db_link = (
            self.db.query(link.Link).filter(link.Link.key == link_key).first()
        )  # noqa: E501
        if db_link is None:
            raise exceptions.LinkNotFoundException()
        db_complaints = (
            self.db.query(complaint.Complaint)
            .filter(complaint.Complaint.link_id == db_link.id)
            .all()
        )
        res = []
        for db_complaint in db_complaints:
            res.append(
                schema.Complaint(
                    id=db_complaint.id,
                    body=db_complaint.body,
                    status=db_complaint.status,
                    link_id=db_complaint.link.id,
                )
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
