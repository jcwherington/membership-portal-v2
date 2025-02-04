import unittest
from unittest.mock import patch, DEFAULT

from api_handler import handle_event
from common.error import ValidationError
from spec_helper import test_event, test_dynamo_entry


class ApiHandlerTest(unittest.TestCase):
    
    def setUp(self):
        self.event = test_event()

    @patch('api_handler.Dynamo')
    def test_handle_event_get(self, dynamo_patch):
        self.event['httpMethod'] = 'GET'
        get_items_mock = dynamo_patch.return_value.get_items
        get_items_mock.return_value = {
            'Items': [
                test_dynamo_entry(),
                test_dynamo_entry(),
                test_dynamo_entry()
            ]
        }

        result = handle_event(self.event)

        self.assertEqual(len(result), 3)
        get_items_mock.assert_called_once()
    
    @patch('api_handler.Dynamo')
    def test_handle_event_post(self, dynamo_patch):
        self.event['httpMethod'] = 'POST'
        put_item_mock = dynamo_patch.return_value.put_item

        handle_event(self.event)

        put_item_mock.assert_called_once()
    
    @patch('api_handler.Dynamo')
    def test_handle_event_delete(self, dynamo_patch):
        self.event['httpMethod'] = 'DELETE'
        delete_item_mock = dynamo_patch.return_value.delete_item

        handle_event(self.event)

        delete_item_mock.assert_called_once()

    def test_handle_event_invalid_http_method(self):
        self.event['httpMethod'] = 'INVALID'

        with self.assertRaises(ValidationError):
            handle_event(self.event)


if __name__ == '__main__':
    unittest.main()
