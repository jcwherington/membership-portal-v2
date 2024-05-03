from db.client import Client
from model.membership import Membership
from common.error import ValidationError


def handle_event(event):
    db_client = Client()

    try:
        if event['httpMethod'] == 'GET':
            return handle_get(event, db_client)

        elif event['httpMethod'] == 'POST':  
            return handle_post(event, db_client)

        elif event['httpMethod'] == 'PUT':
            return handle_put(event, db_client)

        elif event['httpMethod'] == 'DELETE':
            return handle_delete(event, db_client)

        else:
            raise ValidationError('Invalid HTTP method')
    
    finally:
        db_client.close_connection()

def handle_get(event, db_client):
    if event['pathParameters']:
        result = db_client.read(event['pathParameters']['id'])
    else:
        result = db_client.read_all()
    
    return [Membership.serialize(row) for row in result.fetchall()]

def handle_post(event, db_client):
    member = Membership.from_event(event)
    result = db_client.create(member)

    return [Membership.serialize(result.fetchone())]

def handle_put(event, db_client):
    member = Membership.from_event(event)
    result = db_client.update(event['pathParameters']['id'], member)

    return [Membership.serialize(result.fetchone())]

def handle_delete(event, db_client):
    result = db_client.delete(event['pathParameters']['id'])

    return [Membership.serialize(result.fetchone())]
