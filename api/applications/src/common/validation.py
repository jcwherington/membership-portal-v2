from common.error import ValidationError
from datetime import datetime
from config import logger

HTTP_METHODS = ["GET", "POST", "DELETE"]


def validate_event(event):
    match event["httpMethod"]:
        case "GET":
            return
        case "POST":
            validate_post(event)
            return
        case "DELETE":
            validate_delete(event)
            return
        case _:
            raise ValidationError("Invalid HTTP method")


def validate_post(event):
    if not event["body"]:
        raise ValidationError("Request is missing body")

    if not event["body"]["id"]:
        raise ValidationError("Invalid 'id' in body")

    try:
        datetime.strptime(event["body"]["dob"], "%d-%m-%Y")
    except ValueError:
        raise ValidationError("Invalid 'dob' in body")

    try:
        datetime.strptime(event["body"]["createdAt"], "%d-%m-%Y %H:%M:%S")
    except ValueError:
        raise ValidationError("Invalid 'createdAt' in body")


def validate_delete(event):
    if not event["pathParameters"]:
        raise ValidationError("Request URL is missing path parameter")

    if not event["pathParameters"]["id"]:
        raise ValidationError("Invalid 'id' in path parameter")

    if (
        event["queryStringParameters"]
        and not event["queryStringParameters"]["notify"] == "true"
    ):
        raise ValidationError(
            f"invalid value for notify query string parameter: {event['queryStringParameters']['notify']}"
        )
