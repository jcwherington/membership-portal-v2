import unittest
from unittest.mock import patch

from common.validation import validate_event, validate_body
from spec_helper import test_event, test_body
from common.error import ValidationError


class EventValidationTest(unittest.TestCase):
    
    def setUp(self):
        self.event = test_event()

    def test_validate_get(self):
        self.event['httpMethod'] = 'GET'
        self.event['pathParameters'] = { 'id': 1 }
        
        try:
            validate_event(self.event)
        except ValidationError:
            self.fail()

    @patch('common.validation.validate_body')
    def test_validate_post(self, validate_body_patch):
        self.event['httpMethod'] = 'POST'
        self.event['body'] = test_body()
        validate_body_patch.return_value = []

        try:
            validate_event(self.event)
        except ValidationError:
            self.fail()
    
    @patch('common.validation.validate_body')
    def test_validate_post_with_valid_notify(self, validate_body_patch):
        self.event['httpMethod'] = 'POST'
        self.event['queryStringParameters']['notify'] = 'true'
        self.event['body'] = test_body()
        validate_body_patch.return_value = []

        try:
            validate_event(self.event)
        except ValidationError:
            self.fail()
    
    @patch('common.validation.validate_body')
    def test_validate_post_with_invalid_notify(self, validate_body_patch):
        self.event['httpMethod'] = 'POST'
        self.event['queryStringParameters']['notify'] = 'invalid'
        self.event['body'] = test_body()
        validate_body_patch.return_value = []

        with self.assertRaises(ValidationError):
            validate_event(self.event)
    
    @patch('common.validation.validate_body')
    def test_validate_put(self, validate_body_patch):
        self.event['httpMethod'] = 'PUT'
        self.event['pathParameters'] = { 'id': 1 }
        self.event['body'] = test_body()
        validate_body_patch.return_value = []

        try:
            validate_event(self.event)
        except ValidationError:
            self.fail()
    
    def test_validate_delete(self):
        self.event['httpMethod'] = 'DELETE'
        self.event['pathParameters'] = { 'id': 1 }

        try:
            validate_event(self.event)
        except ValidationError:
            self.fail()
    
    def test_invalid_http_method(self):
        self.event['httpMethod'] = 'INVALID'

        with self.assertRaises(ValidationError):
            validate_event(self.event)


class BodyValidationTest(unittest.TestCase):
    
    def setUp(self):
        self.body = test_body()
    
    def test_body(self):
        result = validate_body(self.body)
        self.assertEqual(len(result), 0)

    def test_invalid_email(self):
        self.body['email'] = 'invalid email'
        result = validate_body(self.body)

        self.assertEqual(len(result), 1)
        self.assertTrue('email' in result)

    def test_invalid_post_code(self):
        self.body['postCode'] = 'invalid post code'
        result = validate_body(self.body)

        self.assertEqual(len(result), 1)
        self.assertTrue('post code' in result)

    def test_invalid_mobile(self):
        self.body['mobile'] = 'invalid mobile'
        result = validate_body(self.body)

        self.assertEqual(len(result), 1)
        self.assertTrue('mobile' in result)
    
    def test_invalid_dob(self):
        self.body['dob'] = 'invalid dob'
        result = validate_body(self.body)

        self.assertEqual(len(result), 1)
        self.assertTrue('dob' in result)

    def test_missing_first_name(self):
        self.body['firstName'] = None
        result = validate_body(self.body)

        self.assertEqual(len(result), 1)
        self.assertTrue('first name' in result)

    def test_missing_last_name(self):
        self.body['lastName'] = None
        result = validate_body(self.body)

        self.assertEqual(len(result), 1)
        self.assertTrue('last name' in result)
    
    def test_multiple_invalidations(self):
        self.body['firstName'] = None
        self.body['lastName'] = None
        self.body['mobile'] = 'invalid mobile'
        self.body['dob'] = 'invalid dob'
        self.body['postCode'] = 'invalid post code'
        self.body['email'] = 'invalid email'
        result = validate_body(self.body)

        self.assertEqual(len(result), 6)
        self.assertTrue('first name' in result)
        self.assertTrue('last name' in result)
        self.assertTrue('mobile' in result)
        self.assertTrue('dob' in result)
        self.assertTrue('post code' in result)
        self.assertTrue('email' in result)

if __name__ == '__main__':
    unittest.main()
