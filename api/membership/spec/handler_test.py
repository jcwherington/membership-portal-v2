import logging
import json
import unittest
from unittest.mock import patch, MagicMock
from psycopg2.errors import UniqueViolation

from app import handler
from common.error import DatabaseError
from spec_helper import test_event, base_response, test_body


class HandlerTest(unittest.TestCase):

    def setUpClass():
        logging.disable(logging.CRITICAL)
    
    def setUp(self):
        self.event = test_event()

    @patch('app.handle_event')
    def test_handler_get(self, handle_event_patch):
        self.event['httpMethod'] = 'GET'
        handle_event_patch.return_value = [{}]
        result = handler(self.event, {})

        self.assertEqual(result, base_response(200, 'success', [{}]))
    
    @patch('app.handle_event')
    def test_handler_get_with_param(self, handle_event_patch):
        self.event['httpMethod'] = 'GET'
        self.event['pathParameters'] = { 'id': 1 }
        handle_event_patch.return_value = [{}]
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(200, 'success', [{}]))
    
    @patch('app.handle_event')
    def test_handler_post(self, handle_event_patch):
        self.event['httpMethod'] = 'POST'
        self.event['body'] = json.dumps(test_body())
        handle_event_patch.return_value = [{}]
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(200, 'success', [{}]))
    
    @patch('app.handle_event')
    def test_handler_put(self, handle_event_patch):
        self.event['httpMethod'] = 'PUT'
        self.event['pathParameters'] = {'id': 1}
        self.event['body'] = json.dumps(test_body())
        handle_event_patch.return_value = [{}]
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(200, 'success', [{}]))
    
    @patch('app.handle_event')
    def test_handler_delete(self, handle_event_patch):
        self.event['httpMethod'] = 'DELETE'
        self.event['pathParameters'] = { 'id': 1 }
        handle_event_patch.return_value = None
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(200, 'success', None))
    
    def test_handler_invalid(self):
        self.event['httpMethod'] = 'INVALID'
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(400, 'invalid HTTP method', None))
    
    @patch('app.handle_event')
    def test_handler_error(self, handle_event_patch):
        self.event['httpMethod'] = 'GET'
        handle_event_patch.side_effect = Exception("Mocked exception")
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(500, 'an unexpected error occurred', None))
    
    @patch('app.handle_event')
    def test_handler_unique_violation(self, handle_event_patch):
        self.event['httpMethod'] = 'POST'
        self.event['body'] = json.dumps(test_body())

        class MockExceptionClass(MagicMock):
            @property
            def orig(self):
                return UniqueViolation()

        handle_event_patch.side_effect = DatabaseError(MockExceptionClass())
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(400, 'email already exists', None))

    @patch('app.handle_event')
    def test_handler_database_error(self, handle_event_patch):
        self.event['httpMethod'] = 'POST'
        self.event['body'] = json.dumps(test_body())

        class MockExceptionClass(MagicMock):
            @property
            def orig(self):
                return Exception()
        
        handle_event_patch.side_effect = DatabaseError(MockExceptionClass())
        result = handler(self.event, {})
        
        self.assertEqual(result, base_response(500, 'an unexpected error occurred during database operation', None))

if __name__ == '__main__':
    unittest.main()
