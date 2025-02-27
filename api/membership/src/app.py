import json
from typing import List, Dict

from common.validation import validate_event
from api_handler import handle_event
from common.error import ValidationError, DatabaseError, SnsError
from model.response import Response
from config import logger


def handler(event: Dict, _context) -> Response:
    try:
        log = logger()
        log.info(event)

        if event["body"] and type(event["body"]) == str:
            event["body"] = json.loads(event["body"])

        validate_event(event)
        data: List[Dict] = handle_event(event)

    except ValidationError as error:
        log.error(error._message)
        return Response(400, error._message).resolve()

    except DatabaseError as error:
        log.error(error._message)
        return Response(error._status, error._message).resolve()

    except SnsError as error:
        log.error(error._message)
        return Response(500, error._message).resolve()

    except Exception as error:
        log.error(error)
        return Response(500, "an unexpected error occurred").resolve()

    return Response(200, "success", data).resolve()
