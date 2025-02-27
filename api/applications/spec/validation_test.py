import unittest

from common.validation import validate_event
from common.error import ValidationError
from spec_helper import test_event


class EventValidationTest(unittest.TestCase):

    def setUp(self):
        self.event = test_event()

    def test_validate_event(self):
        try:
            validate_event(self.event)
        except ValidationError:
            self.fail()

    def test_invalid_http_method(self):
        self.event["httpMethod"] = "INVALID"

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    # POST

    def test_POST_missing_body(self):
        self.event["body"] = {}

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    def test_POST_invalid_id_value(self):
        self.event["httpMethod"] = "POST"
        self.event["body"]["id"] = None

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    def test_POST_invalid_dob_value(self):
        self.event["httpMethod"] = "POST"
        self.event["body"]["dob"] = ""

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    def test_POST_invalid_createdAt_value(self):
        self.event["httpMethod"] = "POST"
        self.event["body"]["createdAt"] = ""

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    # DELETE

    def test_DELETE_missing_path_parameter(self):
        self.event["httpMethod"] = "DELETE"
        self.event["pathParameters"] = {}

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    def test_DELETE_invalid_id_value(self):
        self.event["httpMethod"] = "DELETE"
        self.event["pathParameters"]["id"] = None

        with self.assertRaises(ValidationError):
            validate_event(self.event)

    def test_DELETE_with_invalid_notify(self):
        self.event["httpMethod"] = "DELETE"
        self.event["queryStringParameters"]["notify"] = "invalid"
        self.event["pathParameters"]["id"] = "1"

        with self.assertRaises(ValidationError):
            validate_event(self.event)


if __name__ == "__main__":
    unittest.main()
