from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class Application:
    _id: int
    _first_name: str
    _last_name: str
    _email: str
    _organisation: str
    _position: str
    _industry: str
    _dob: datetime
    _mobile: str
    _city: str
    _post_code: str
    _created_at: datetime

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def email(self):
        return self._email

    @property
    def organisation(self):
        return self._organisation

    @property
    def position(self):
        return self._position

    @property
    def industry(self):
        return self._industry

    @property
    def dob(self):
        return self._dob

    @property
    def mobile(self):
        return self._mobile

    @property
    def city(self):
        return self._city

    @property
    def post_code(self):
        return self._post_code

    @property
    def created_at(self):
        return self._created_at

    @classmethod
    def from_event(cls, event: Dict) -> "Application":
        applicant_data = event["body"]

        return cls(
            applicant_data["id"],
            applicant_data["firstName"],
            applicant_data["lastName"],
            applicant_data["email"],
            applicant_data["organisation"],
            applicant_data["position"],
            applicant_data["industry"],
            applicant_data["dob"],
            applicant_data["mobile"],
            applicant_data["city"],
            applicant_data["postCode"],
            applicant_data["createdAt"],
        )

    @classmethod
    def from_dynamo(cls, item) -> Dict[str, Any]:
        return {
            "firstName": item["first_name"]["S"],
            "lastName": item["last_name"]["S"],
            "email": item["email"]["S"],
            "organisation": item["organisation"]["S"],
            "position": item["position"]["S"],
            "industry": item["industry"]["S"],
            "dob": item["dob"]["S"],
            "mobile": item["mobile"]["S"],
            "city": item["city"]["S"],
            "postCode": item["post_code"]["S"],
            "createdAt": item["created_at"]["S"],
            "id": item["id"]["S"],
        }

    def to_dynamo(self) -> Dict[str, Any]:
        return {
            "id": {
                "S": self.id,
            },
            "first_name": {
                "S": self.first_name,
            },
            "last_name": {
                "S": self.last_name,
            },
            "organisation": {
                "S": self.organisation,
            },
            "industry": {
                "S": self.industry,
            },
            "position": {
                "S": self.position,
            },
            "email": {
                "S": self.email,
            },
            "mobile": {
                "S": self.mobile,
            },
            "post_code": {
                "S": self.post_code,
            },
            "dob": {
                "S": self.dob,
            },
            "created_at": {
                "S": self.created_at,
            },
            "city": {
                "S": self.city,
            },
        }
