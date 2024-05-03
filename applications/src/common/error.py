class ValidationError(Exception):
    def __init__(self, message):
        self.message = message

class DynamoError(Exception):
    def __init__(self, message):
        self.message = message
