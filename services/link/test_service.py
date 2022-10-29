import unittest

import pytest

from infrastructure.CassandraDB import get_cassandra_db
from infrastructure.db import Base
from models import link, user
from services.link import exceptions, schema, service


class TestLinkService(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def db_setup(self, db_session_factory):
        self.db = db_session_factory()
        self.engine = self.db.get_bind()

    def setUp(self) -> None:
        Base.metadata.create_all(self.engine)
        # Get cassandra session
        self.cassandra_session = get_cassandra_db()
        # Connect to database and initialize service
        self.service = service.Service(self.db, self.cassandra_session)
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
        stmt = self.cassandra_session.prepare(
            "INSERT INTO urls (key, reference, action, owner_id,is_active) VALUES (?,?,?,?,?);"  # noqa:E501
        )
        self.cassandra_session.execute(
            stmt,
            (
                self.link1.key,
                self.link1.reference,
                self.link1.action,
                self.link1.owner_id,
                self.link1.is_active,
            ),
        )
        self.db.add(self.user1)
        self.db.add(self.user2)
        self.db.add(self.link1)
        self.db.commit()

    def test_create_link(self):
        """Test if user can create a link"""
        inp = schema.CreateLinkSchema(
            reference="http://test.com",
            is_active=True,
        )
        res = self.service.create_link(inp, 1)
        db_link = (
            self.db.query(link.Link)
            .filter(link.Link.key == res.key)
            .first()  # noqa:E501
        )
        self.assertIsNotNone(db_link)
        self.assertEqual(db_link.action, "REDIRECT")

    def tearDown(self) -> None:
        self.db.rollback()
        self.db.close()
        Base.metadata.drop_all(self.engine)
        # Clear url table
        self.cassandra_session.execute("TRUNCATE urls")

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

    def test_get_all_links(self):
        """Test if all links can be retreived"""
        res = self.service.get_all_links()
        self.assertIsNotNone(res)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].reference, "http://test.com")

    def test_update_link(self):
        """Test if link can be updated"""
        inp = schema.UpdateLinkSchema(
            key="testlink123",
            action="BLOCK",
        )
        res = self.service.update_link_action_by_key(inp)
        self.assertIsNotNone(res)
        self.assertEqual(res.action, "BLOCK")
        inp = schema.UpdateLinkSchema(
            key="testlink",
            action="BLOCK",
        )
        self.assertRaises(
            exceptions.LinkNotFoundException,
            self.service.update_link_action_by_key,
            inp,  # noqa:E501
        )

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
