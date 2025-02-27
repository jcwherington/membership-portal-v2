import unittest
from unittest.mock import patch
from botocore.exceptions import ClientError

from services.dynamo import Dynamo
from spec_helper import test_event, get_item, init_database
from model.application import Application
from common.error import DynamoError


class DynamoTest(unittest.TestCase):

    def setUp(self):
        self.event = test_event()
        self.applicant = Application.from_event(self.event)
        self.dynamo = Dynamo()
        init_database(self.dynamo.client)

    def test_put_item(self):
        self.dynamo.put_item(self.applicant)
        result = get_item(self.dynamo.client, self.applicant.id)

        self.assertIn("Item", result)

    def test_get_items(self):
        result = self.dynamo.get_items()

        self.assertTrue(len(result["Items"]) > 0)

    def test_delete_item(self):
        self.dynamo.delete_item("10")
        result = get_item(self.dynamo.client, "10")

        self.assertNotIn("Item", result)

    @patch("botocore.client.BaseClient._make_api_call")
    def test_dynamo_error(self, mock):
        mock.side_effect = ClientError(
            error_response={"Error": {"Message": "error"}}, operation_name="mock_op"
        )

        with self.assertRaises(DynamoError):
            self.dynamo.put_item(self.applicant)


if __name__ == "__main__":
    unittest.main()
