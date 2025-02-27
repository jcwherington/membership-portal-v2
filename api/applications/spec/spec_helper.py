import json

from config import table_name


def test_event():
    return {
        "resource": "/membership/applications",
        "path": "/membership/applications",
        "httpMethod": 'POST',
        "queryStringParameters": {},
        "multiValueQueryStringParameters": None,
        "pathParameters": {
            'id': 1
        },
        "body": {
            'firstName': 'John',
            'lastName': 'Doe',
            'organisation': 'Johns Accounting',
            'position': 'President', 
            'industry': 'Accounting',
            'mobile': '0401999464',
            'dob': '16-02-1994',
            'city': 'Newcastle',
            'postCode': '1234',
            'email': 'john.doe@example.com',
            'id': '2268',
            'createdAt': '16-07-2023 06:34:00'
        }
    }

def test_dynamo_entry():
    return {
        'city': {'S': 'Newcastle'},
        'mobile': {'S': '0401999464'}, 
        'last_name': {'S': 'Doe'}, 
        'organisation': {'S': 'Johns Accounting'}, 
        'created_at': {'S': '16-07-2023 06:34:00'}, 
        'industry': {'S': 'Accounting'},
        'dob': {'S': '16-02-1994'}, 
        'post_code': {'S': '1234'}, 
        'id': {'S': '2268'}, 
        'position': {'S': 'President'}, 
        'first_name': {'S': 'John'}, 
        'email': {'S': 'john.doe@example.com'}
    }

def base_response(code, message, data):
    return {
        'statusCode': code,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': message,
            'data': data
        })
    }

def init_database(client):
    try:
        client.create_table(
            TableName=table_name(),
            AttributeDefinitions=[{
                'AttributeName': 'id',
                'AttributeType': 'S'
            }],
            KeySchema=[{
                'AttributeName': 'id',
                'KeyType': 'HASH'
            }],
            BillingMode='PAY_PER_REQUEST'
        )
    except client.exceptions.ResourceInUseException:
        pass

    client.put_item(
        TableName=table_name(),
        Item={
            'id': { 'S': '10' }
        }
    )

def get_item(client, id):
    return client.get_item(
        TableName=table_name(),
        Key={
            'id': { 'S': id }
        }
    )
