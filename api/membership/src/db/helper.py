from sqlalchemy import URL, Table, MetaData, Column, Text, DateTime, String, Integer

from config import db_endpoint, db_name, db_port, db_user, db_password, schema


def connection_string():
    return URL.create(
        'postgresql+psycopg2',
        username=db_user(),
        password=db_password(),
        host=db_endpoint(),
        database=db_name(),
        port=db_port()
    )

def table():
    return Table(
        'membership',
        MetaData(),
        Column('member_id', Integer, primary_key=True),
        Column('first_name', Text, nullable=False),
        Column('last_name', Text, nullable=False),
        Column('email', Text, nullable=False),
        Column('organisation', Text),
        Column('position', Text),
        Column('industry', Text),
        Column('dob', DateTime, nullable=False),
        Column('mobile', String(10)),
        Column('city', Text),
        Column('post_code', String(4)),
        Column('created_at', DateTime),
        Column('updated_at', DateTime),
        schema=schema()
    )

def columns(table):
    return [
        table.c.member_id,
        table.c.first_name,
        table.c.last_name,
        table.c.email,
        table.c.organisation,
        table.c.position,
        table.c.industry,
        table.c.dob,
        table.c.mobile,
        table.c.city,
        table.c.post_code,
        table.c.created_at,
        table.c.updated_at
    ]
