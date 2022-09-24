import unittest

import pytest

from infrastructure.db import Base
from models import link, user
from services.link import exceptions, schema, service


class TestUserService(unittest.TestCase):
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

    def test_create_link(self):
        """Test if user can be created"""
        inp = schema.CreateLinkSchema(
            reference="http://test.com",
            owner_id=self.user1.id,
            action="REDIRECT",
        )
        res = self.service.create_link(inp)
        db_link = (
            self.db.query(link.Link)
            .filter(link.Link.key == res.key)
            .first()  # noqa:E501
        )
        self.assertIsNotNone(db_link)

    def tearDown(self) -> None:
        self.db.rollback()
        self.db.close()
        Base.metadata.drop_all(self.engine)

    def test_get_link_by_key(self):
        """Test if a link can be retreived by key"""
        res = self.service.get_link_by_key("testlink123")
        self.assertIsNotNone(res)
        self.assertEqual(res.reference, "http://test.com")
        self.assertRaises(
            exceptions.LinkNotFoundException,
            self.service.get_link_by_key,
            "testlink345",  # noqa:E501
        )

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
