from sqlalchemy import insert, delete, update, select


class StatementGenerator:

    def __init__(self, table):
        self._table = table

    def insert(self, data):
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

    def delete(self, id):
        return delete(self._table).where(self._table.c.member_id == id)

    def update(self, data, id):
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

    def select_one(self, id):
        return select(self._table).where(self._table.c.member_id == id)

    def select_all(self):
        return select(self._table)
