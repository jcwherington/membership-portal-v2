import json
from logging import Logger
from typing import List, Dict

from common.validation import validate_event
from api_handler import handle_event
from common.error import ValidationError, DynamoError, SnsError
from model.response import Response
from model.application import Application
from config import logger


def handler(event: Dict, _context) -> Response:
    try:
        log: Logger = logger()
        log.info(event)

        if event["body"] and type(event["body"]) == str:
            event["body"] = json.loads(event["body"])

        validate_event(event)
        data: List[Application]|None = handle_event(event)

    except ValidationError as error:
        log.error(error.message)
        return Response(400, error.message).resolve()

    except DynamoError as error:
        log.error(error.message)
        return Response(500, error.message).resolve()

    except SnsError as error:
        log.error(error.message)
        return Response(500, error.message).resolve()

    except Exception as error:
        log.error(error)
        return Response(500, "an unexpected error occurred").resolve()

    return Response(200, "success", data).resolve()
