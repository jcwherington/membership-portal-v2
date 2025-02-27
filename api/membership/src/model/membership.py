from dataclasses import dataclass, fields
from datetime import datetime, date
from typing import Dict
import humps


@dataclass
class Membership:
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
    _updated_at: datetime

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

    @property
    def updated_at(self):
        return self._updated_at

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @email.setter
    def email(self, email):
        self._email = email

    @organisation.setter
    def organisation(self, organisation):
        self._organisation = organisation

    @position.setter
    def position(self, position):
        self._position = position

    @industry.setter
    def industry(self, industry):
        self._industry = industry

    @dob.setter
    def dob(self, dob):
        self._dob = dob

    @mobile.setter
    def mobile(self, mobile):
        self._mobile = mobile

    @post_code.setter
    def post_code(self, post_code):
        self._post_code = post_code

    @created_at.setter
    def created_at(self, created_at):
        self._created_at = created_at

    @updated_at.setter
    def updated_at(self, updated_at):
        self._updated_at = updated_at

    @classmethod
    def from_event(cls, event) -> "Membership":
        member_data = event["body"]

        return cls(
            member_data["firstName"],
            member_data["lastName"],
            member_data["email"],
            member_data["organisation"],
            member_data["position"],
            member_data["industry"],
            member_data["dob"],
            member_data["mobile"],
            member_data["city"],
            member_data["postCode"],
            str(datetime.now()),
            str(datetime.now()),
        )

    @classmethod
    def serialize(cls, tuple) -> Dict:
        property_names = [
            humps.camelize(field.name.lstrip("_")) for field in fields(cls)
        ]
        property_names.insert(0, "id")
        member_dict = {
            key: value.isoformat() if isinstance(value, date) else value
            for key, value in zip(property_names, tuple)
        }

        return member_dict
