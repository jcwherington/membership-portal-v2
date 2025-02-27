import unittest

from model.membership import Membership
from spec_helper import test_event, test_body, test_tuple


class MembershipTest(unittest.TestCase):

    def test_from_event(self):
        event = test_event()
        event["body"] = test_body()
        member = Membership.from_event(event)

        self.assertEqual(member.first_name, "John")
        self.assertEqual(member.last_name, "Doe")
        self.assertEqual(member.email, "john.doe@example.com")
        self.assertEqual(member.organisation, "Johns Accounting")
        self.assertEqual(member.position, "President")
        self.assertEqual(member.industry, "Accounting")
        self.assertEqual(member.dob, "01-01-2000")
        self.assertEqual(member.mobile, "0401999464")
        self.assertEqual(member.city, "Newcastle")
        self.assertEqual(member.post_code, "1234")

    def test_serialize(self):
        member_dict = Membership.serialize(test_tuple())

        self.assertEqual(member_dict["id"], 1)
        self.assertEqual(member_dict["firstName"], "John")
        self.assertEqual(member_dict["lastName"], "Doe")
        self.assertEqual(member_dict["email"], "john.doe@example.com")
        self.assertEqual(member_dict["organisation"], "Johns Accounting")
        self.assertEqual(member_dict["position"], "President")
        self.assertEqual(member_dict["industry"], "Accounting")
        self.assertEqual(member_dict["dob"], "01-01-2000")
        self.assertEqual(member_dict["mobile"], "0401999464")
        self.assertEqual(member_dict["city"], "Newcastle")
        self.assertEqual(member_dict["postCode"], "1234")
        self.assertEqual(member_dict["createdAt"], "2023-05-17 10:20:31.763416")
        self.assertEqual(member_dict["updatedAt"], "2023-05-17 10:20:31.763429")


if __name__ == "__main__":
    unittest.main()
