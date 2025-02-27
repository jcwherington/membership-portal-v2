from sqlalchemy import insert, delete, update, select, Table

from model.membership import Membership


class StatementGenerator:

    def __init__(self, table: Table) -> None:
        self._table = table

    def insert(self, data: Membership) -> str:
        return insert(self._table).values(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            organisation=data.organisation,
            position=data.position,
            industry=data.industry,
            dob=data.dob,
            mobile=data.mobile,
            city=data.city,
            post_code=data.post_code,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )

    def delete(self, id: int) -> str:
        return delete(self._table).where(self._table.c.member_id == id)

    def update(self, data: Membership, id: int) -> str:
        return (
            update(self._table)
            .where(self._table.c.member_id == id)
            .values(
                first_name=data.first_name,
                last_name=data.last_name,
                email=data.email,
                organisation=data.organisation,
                position=data.position,
                industry=data.industry,
                dob=data.dob,
                mobile=data.mobile,
                city=data.city,
                post_code=data.post_code,
                updated_at=data.updated_at,
            )
        )

    def select_one(self, id: int) -> str:
        return select(self._table).where(self._table.c.member_id == id)

    def select_all(self) -> str:
        return select(self._table)
