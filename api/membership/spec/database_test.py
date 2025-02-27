import unittest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError

from db.client import Client
from spec_helper import (
    test_event,
    test_body,
    expected_membership_keys,
    populate_database,
)
from model.membership import Membership
from common.error import DatabaseError


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.event = test_event()
        self.event["body"] = test_body()
        self.member = Membership.from_event(self.event)

    def test_create(self):
        client = Client()

        result = client.create(self.member)
        as_dict = Membership.serialize(result.fetchone())

        self.assertTrue(
            all(key in as_dict.keys() for key in expected_membership_keys())
        )

    def test_read(self):
        client = Client()
        client.execute(populate_database(8))

        result = client.read(8)
        as_dict = Membership.serialize(result.fetchone())

        self.assertTrue(
            all(key in as_dict.keys() for key in expected_membership_keys())
        )

    def test_read_all(self):
        client = Client()
        client.execute(populate_database(7))

        result = client.read_all()
        as_dict = Membership.serialize(result.fetchone())

        self.assertTrue(
            all(key in as_dict.keys() for key in expected_membership_keys())
        )

    def test_update(self):
        client = Client()
        client.execute(populate_database(6))

        self.member.first_name = "Jane"
        self.member.email = "jane.doe@example.com"

        result = client.update(6, self.member)
        as_dict = Membership.serialize(result.fetchone())

        self.assertTrue(
            all(key in as_dict.keys() for key in expected_membership_keys())
        )

    def test_delete(self):
        client = Client()
        client.execute(populate_database(5))

        result = client.delete(5)
        as_dict = Membership.serialize(result.fetchone())

        self.assertTrue(
            all(key in as_dict.keys() for key in expected_membership_keys())
        )

    def test_delete_missing(self):
        client = Client()
        result = client.delete(6)

        self.assertIsNone(result.fetchone())

    def test_update_unique_violation(self):
        client = Client()
        mock_exception = IntegrityError("", (""), Exception())

        with patch.object(Client, "execute", side_effect=mock_exception):
            with self.assertRaises(DatabaseError):
                client.update(6, self.member)

    def test_create_unique_violation(self):
        client = Client()
        mock_exception = IntegrityError("", (""), Exception())

        with patch.object(Client, "execute", side_effect=mock_exception):
            with self.assertRaises(DatabaseError):
                client.create(self.member)


if __name__ == "__main__":
    unittest.main()
