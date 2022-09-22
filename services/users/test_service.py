import unittest

import pytest

from infrastructure.db import Base
from models import user
from services.users import exceptions, schema, service


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
        self.db.add(self.user1)
        self.db.add(self.user2)
        self.db.commit()

    def test_create_user(self):
        """Test if user can be created"""
        inp = schema.CreateUserSchema(
            username="test",
            email="test@test.com",
            is_admin=True,
            password="test123",  # noqa:E501
        )
        self.service.create_user(inp)
        db_user = (
            self.db.query(user.User)
            .filter(user.User.email == "test@test.com")
            .first()  # noqa:E501
        )
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, "test")

    def test_get_user_by_id(self):
        """Test if a user can be retreived by id"""
        db_user = self.service.get_user_by_id(self.user1.id)
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user1.username)
        self.assertRaises(
            exceptions.UserNotFoundException, self.service.get_user_by_id, 5
        )

    def test_get_user_by_username(self):
        """Test if a user can be retreived by username"""
        db_user = self.service.get_user_by_username(self.user1.username)
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.username, self.user1.username)
        self.assertRaises(
            exceptions.UserNotFoundException,
            self.service.get_user_by_username,
            "test5",  # noqa:E501
        )

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

    def tearDown(self) -> None:
        self.db.rollback()
        self.db.close()
        Base.metadata.drop_all(self.engine)
