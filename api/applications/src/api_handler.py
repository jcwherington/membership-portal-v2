from typing import List, Dict

from model.application import Application
from services.dynamo import Dynamo
from services.sns import Sns
from common.error import ValidationError


def handle_event(event: Dict) -> List[Application]|None:
    dynamo = Dynamo()

    match event["httpMethod"]:
        case "GET":
            return handle_get(dynamo)
        case "POST":
            handle_post(event, dynamo)
            return
        case "DELETE":
            handle_delete(event, dynamo)
            return
        case _:
            raise ValidationError("Invalid HTTP method")


def handle_get(dynamo: Dynamo) -> List[Application]:
    result = dynamo.get_items()

    data = []
    if result["Items"]:
        for applicant_data in result["Items"]:
            applicant = Application.from_dynamo(applicant_data)
            data.append(applicant)

    return data


def handle_post(event: Dict, dynamo: Dynamo) -> None:
    applicant = Application.from_event(event)
    dynamo.put_item(applicant)


def handle_delete(event: Dict, dynamo: Dynamo) -> None:
    result = dynamo.delete_item(event["pathParameters"]["id"])

    if "notify" in event["queryStringParameters"]:
        name = (
            result["Attributes"]["first_name"]["S"]
            + " "
            + result["Attributes"]["last_name"]["S"]
        )
        recipient = result["Attributes"]["email"]["S"]

        message_attributes = {
            "Name": {"DataType": "String", "StringValue": name},
            "Recipient": {"DataType": "String", "StringValue": recipient},
        }

        Sns().notify_outcome(message_attributes)
