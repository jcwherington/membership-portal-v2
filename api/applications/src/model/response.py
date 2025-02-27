import json
from typing import Dict


class Response:
    def __init__(self, code: int, message: str, data=None):
        self._status_code = code
        self._message = message
        self._data = data

    def resolve(self) -> Dict:
        return {
            "statusCode": self._status_code,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"message": self._message, "data": self._data}),
        }
