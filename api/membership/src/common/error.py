from psycopg2.errors import UniqueViolation

class ValidationError(Exception):
    def __init__(self, message):
        self._message = message

class DatabaseError(Exception):
    def __init__(self, error):
        if type(error.orig) == UniqueViolation:
            self._message = 'email already exists'
            self._status = 400
        else:
            self._message = 'an unexpected error occurred during database operation'
            self._status = 500

class SnsError(Exception):
    def __init__(self, message):
        self._message = message
