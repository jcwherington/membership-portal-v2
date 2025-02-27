from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError

from db.helper import connection_string, table, columns
from model.membership import Membership
from common.error import DatabaseError
from db.statement_generator import StatementGenerator


class Client:

    def __init__(self) -> None:
        self._engine = create_engine(connection_string())
        self._table = table()
        self._generator = StatementGenerator(self._table)

    def execute(self, statement):
        result = []
        with self._engine.connect() as connection:
            result = connection.execute(statement)
            connection.commit()
            connection.close()

        return result

    def read(self, id: int):
        statement = self._generator.select_one(id)

        return self.execute(statement)

    def read_all(self):
        statement = self._generator.select_all()

        return self.execute(statement)

    def create(self, member: Membership):
        statement = self._generator.insert(member)

        try:
            return self.execute(statement.returning(*columns(self._table)))

        except IntegrityError as error:
            raise DatabaseError(error)

    def delete(self, id: int):
        statement = self._generator.delete(id)

        return self.execute(statement.returning(*columns(self._table)))

    def update(self, id: int, member: Membership):
        statement = self._generator.update(member, id)

        try:
            return self.execute(statement.returning(*columns(self._table)))

        except IntegrityError as error:
            raise DatabaseError(error)

    def close_connection(self) -> None:
        self._engine.dispose()
