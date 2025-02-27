import json

from sqlalchemy import text


def test_event():
    return {
        "resource": "/",
        "path": "/",
        "httpMethod": None,
        "queryStringParameters": {},
        "multiValueQueryStringParameters": None,
        "pathParameters": None,
        "body": "",
    }


def base_response(code, message, data):
    return {
        "statusCode": code,
        "body": json.dumps({"message": message, "data": data}),
        "headers": {"Access-Control-Allow-Origin": "*"},
    }


def test_body():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "organisation": "Johns Accounting",
        "position": "President",
        "industry": "Accounting",
        "dob": "01-01-2000",
        "mobile": "0401999464",
        "city": "Newcastle",
        "postCode": "1234",
    }


def expected_membership_keys():
    return [
        "firstName",
        "lastName",
        "email",
        "organisation",
        "position",
        "industry",
        "dob",
        "mobile",
        "city",
        "postCode",
        "createdAt",
        "updatedAt",
    ]


def test_tuple():
    return (
        1,
        "John",
        "Doe",
        "john.doe@example.com",
        "Johns Accounting",
        "President",
        "Accounting",
        "01-01-2000",
        "0401999464",
        "Newcastle",
        "1234",
        "2023-05-17 10:20:31.763416",
        "2023-05-17 10:20:31.763429",
    )


def populate_database(id):
    return text(
        f"INSERT INTO test.membership (member_id, first_name, last_name, email, organisation, position, industry, dob, mobile, city, post_code, created_at, updated_at) VALUES({id}, 'Bob', 'Jones', 'bobjones@example.com', 'AcmeCorp', 'Manager', 'Technology', '1985-10-15', '1234567890', 'Sydney', '1234', '2021-01-01', '2021-01-02');"
    )
