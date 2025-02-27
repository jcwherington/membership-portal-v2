from typing import List, Dict
from db.client import Client
from services.sns import Sns
from model.membership import Membership
from common.error import ValidationError


def handle_event(event: Dict) -> List[Dict]:
    db_client = Client()

    try:
        match event["httpMethod"]:
            case "GET":
                return handle_get(event, db_client)
            case "POST":
                return handle_post(event, db_client)
            case "PUT":
                return handle_put(event, db_client)
            case "DELETE":
                return handle_delete(event, db_client)
            case _:
                raise ValidationError("Invalid HTTP method")
    finally:
        db_client.close_connection()


def handle_get(event: Membership, db_client: Client) -> List[Dict]:
    if event["pathParameters"]:
        result = db_client.read(event["pathParameters"]["id"])
    else:
        result = db_client.read_all()

    return [Membership.serialize(row) for row in result.fetchall()]


def handle_post(event: Membership, db_client: Client) -> List[Dict]:
    member = Membership.from_event(event)
    result = db_client.create(member)

    if "notify" in event["queryStringParameters"]:
        name = member.first_name + " " + member.last_name
        message_attributes = {
            "Name": {"DataType": "String", "StringValue": name},
            "Recipient": {"DataType": "String", "StringValue": member.email},
        }

        Sns().notify_outcome(message_attributes)

    return [Membership.serialize(result.fetchone())]


def handle_put(event: Membership, db_client: Client) -> List[Dict]:
    member = Membership.from_event(event)
    result = db_client.update(event["pathParameters"]["id"], member)

    return [Membership.serialize(result.fetchone())]


def handle_delete(event: Membership, db_client: Client) -> List[Dict]:
    result = db_client.delete(event["pathParameters"]["id"])

    return [Membership.serialize(result.fetchone())]
