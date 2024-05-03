import unittest

from model.application import Application
from spec_helper import test_event, test_dynamo_entry


class ApplicationTest(unittest.TestCase):
    
    def test_from_event(self):
        event = test_event()
        application = Application.from_event(event)

        self.assertEqual(application.id, '2268')
        self.assertEqual(application.first_name, 'John')
        self.assertEqual(application.last_name, 'Doe')
        self.assertEqual(application.email, 'john.doe@example.com')
        self.assertEqual(application.organisation, 'Johns Accounting')
        self.assertEqual(application.position, 'President')
        self.assertEqual(application.industry, 'Accounting')
        self.assertEqual(application.dob, '1994-02-16')
        self.assertEqual(application.mobile, '0401999464')
        self.assertEqual(application.city, 'Newcastle')
        self.assertEqual(application.post_code, '1234')
        self.assertEqual(application.created_at, '2023-07-16 06:34:00')
    
    def test_to_dynamo(self):
        event = test_event()
        application = Application.from_event(event)
        dynamo_entry = application.to_dynamo()
        
        self.assertEqual(dynamo_entry['id']['S'], '2268')
        self.assertEqual(dynamo_entry['first_name']['S'], 'John')
        self.assertEqual(dynamo_entry['last_name']['S'], 'Doe')
        self.assertEqual(dynamo_entry['email']['S'], 'john.doe@example.com')
        self.assertEqual(dynamo_entry['organisation']['S'], 'Johns Accounting')
        self.assertEqual(dynamo_entry['position']['S'], 'President')
        self.assertEqual(dynamo_entry['industry']['S'], 'Accounting')
        self.assertEqual(dynamo_entry['dob']['S'], '1994-02-16')
        self.assertEqual(dynamo_entry['mobile']['S'], '0401999464')
        self.assertEqual(dynamo_entry['city']['S'], 'Newcastle')
        self.assertEqual(dynamo_entry['post_code']['S'], '1234')
        self.assertEqual(dynamo_entry['created_at']['S'], '2023-07-16 06:34:00')
    
    def test_from_dynamo(self):
        dynamo_entry = test_dynamo_entry()
        application = Application.from_dynamo(dynamo_entry)

        self.assertEqual(application['id'], '2268')
        self.assertEqual(application['firstName'], 'John')
        self.assertEqual(application['lastName'], 'Doe')
        self.assertEqual(application['email'], 'john.doe@example.com')
        self.assertEqual(application['organisation'], 'Johns Accounting')
        self.assertEqual(application['position'], 'President')
        self.assertEqual(application['industry'], 'Accounting')
        self.assertEqual(application['dob'], '1994-02-16')
        self.assertEqual(application['mobile'], '0401999464')
        self.assertEqual(application['city'], 'Newcastle')
        self.assertEqual(application['postCode'], '1234')
        self.assertEqual(application['createdAt'], '2023-07-16 06:34:00')

if __name__ == '__main__':
    unittest.main()
