import logging
import json
import unittest
from unittest.mock import patch

from app import handler
from common.error import DynamoError
from spec_helper import test_event, base_response


class HandlerTest(unittest.TestCase):

    def setUpClass():
        logging.disable(logging.CRITICAL)

    def setUp(self):
        self.event = test_event()
        self.event["body"] = json.dumps(self.event["body"])

    @patch("app.handle_event")
    def test_handler_get(self, handle_event_patch):
        self.event["httpMethod"] = "GET"
        handle_event_patch.return_value = [{}]
        result = handler(self.event, {})

        self.assertEqual(result, base_response(200, "success", [{}]))

    @patch("app.handle_event")
    def test_handler_post(self, handle_event_patch):
        self.event["httpMethod"] = "POST"
        handle_event_patch.return_value = None
        result = handler(self.event, {})

        self.assertEqual(result, base_response(200, "success", None))

    @patch("app.handle_event")
    def test_handler_delete(self, handle_event_patch):
        self.event["httpMethod"] = "DELETE"
        self.event["pathParameters"]["id"] = "1"
        handle_event_patch.return_value = None
        result = handler(self.event, {})

        self.assertEqual(result, base_response(200, "success", None))

    def test_handler_invalid(self):
        self.event["httpMethod"] = "INVALID"
        result = handler(self.event, {})

        self.assertEqual(result, base_response(400, "Invalid HTTP method", None))

    @patch("app.handle_event")
    def test_handler_error(self, handle_event_patch):
        self.event["httpMethod"] = "GET"
        handle_event_patch.side_effect = Exception("Mocked exception")
        result = handler(self.event, {})

        self.assertEqual(
            result, base_response(500, "an unexpected error occurred", None)
        )

    @patch("app.handle_event")
    def test_handler_database_error(self, handle_event_patch):
        self.event["httpMethod"] = "GET"

        handle_event_patch.side_effect = DynamoError("a database error occurred")
        result = handler(self.event, {})

        self.assertEqual(result, base_response(500, "a database error occurred", None))


if __name__ == "__main__":
    unittest.main()
