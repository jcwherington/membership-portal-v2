class ValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class DynamoError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class SnsError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
