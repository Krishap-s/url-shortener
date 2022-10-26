import unittest

import pytest

from infrastructure.db import Base
from models import complaint, link, user
from services.complaint import schema, service


class TestComplaintService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def db_setup(self, db_session_factory):
        self.db = db_session_factory()
        self.engine = self.db.get_bind()

    def setUp(self) -> None:
        Base.metadata.create_all(self.engine)
        # Connect to database and initialize service
        self.service = service.Service(self.db)
        # Insert test data
        # Password:"hello"
        self.user1 = user.User(
            username="test1",
            hashed_password="$2a$12$6UVnRscNBd8bay6evGch8uvJe6fvCPXYD7S43LP4j6IGmhmKaQ3tm",  # noqa:E501
            email="test1@test.com",
        )
        self.user2 = user.User(
            username="test2",
            hashed_password="$2a$12$6UVnRscNBd8bay6evGch8uvJe6fvCPXYD7S43LP4j6IGmhmKaQ3tm",  # noqa:E501
            email="test2@test.com",
        )
        self.link1 = link.Link(
            key="testlink123",
            reference="http://test.com",
            owner_id=1,
            action="REDIRECT",
            is_active=True,
        )

        self.db.add(self.user1)
        self.db.add(self.user2)
        self.db.add(self.link1)
        self.db.commit()
        self.db.refresh(self.link1)
        self.complaint1 = complaint.Complaint(
            body="test234",
            status="PENDING",
            link_id=self.link1.id,
        )
        self.complaint2 = complaint.Complaint(
            body="test345",
            status="PENDING",
            link_id=self.link1.id,
        )
        self.db.add(self.complaint1)
        self.db.add(self.complaint2)
        self.db.commit()
        self.db.refresh(self.complaint1)
        self.db.refresh(self.complaint2)

    def test_create_complaint(self):
        """Test if user can create a complaint"""
        inp = schema.CreateComplaintSchema(
            link_key=self.link1.key, body="test123"
        )  # noqa:E501
        res = self.service.create_complaint(inp)
        db_complaint = (
            self.db.query(complaint.Complaint)
            .filter(complaint.Complaint.id == res.id)
            .first()  # noqa:E501
        )
        self.assertIsNotNone(db_complaint)
        self.assertEqual(db_complaint.body, "test123")
        self.assertEqual(db_complaint.link_id, self.link1.id)

    def tearDown(self) -> None:
        self.db.rollback()
        self.db.close()
        Base.metadata.drop_all(self.engine)

    def test_get_complaints_by_link_key(self):
        """Test if a link can be retreived by key"""
        res = self.service.get_complaints_by_link(self.link1.key)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].body, "test234")
        self.assertEqual(res[1].body, "test345")

    # TODO: Remove commented code
    '''

    def test_get_user_by_email(self):
        """Test if a user can be retreived by email"""
        db_user = self.service.get_user_by_email(self.user1.email)
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user1.username)
        self.assertRaises(
            exceptions.UserNotFoundException,
            self.service.get_user_by_email,
            "test5@test.com",
        )

    def test_authenticate(self):
        """Test if a user can be authenticated"""
        creds = schema.AuthenticateSchema(
            username=self.user1.username, password="hello"
        )
        db_user = self.service.authenticate(creds)
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user1.username)
        invalid_creds = schema.AuthenticateSchema(
            username=self.user1.username, password="hello2"
        )
        self.assertRaises(
            exceptions.InvalidCredentials,
            self.service.authenticate,
            invalid_creds,  # noqa:E501
        )
'''
