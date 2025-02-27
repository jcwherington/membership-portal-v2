import sys
import logging
import os


def region():
    return "us-west-2"


def db_endpoint():
    return os.getenv("DB_ENDPOINT")


def db_port():
    return os.getenv("DB_PORT")


def db_name():
    return os.getenv("DB_NAME")


def db_user():
    return os.getenv("DB_USER")


def db_password():
    return os.getenv("DB_PASSWORD")


def branch():
    return os.getenv("BRANCH")


def sns_topic_arn():
    return os.getenv("SNS_TOPIC_ARN")


def schema():
    match branch():
        case "local":
            return "local"
        case "main":
            return "prod"
        case _:
            return "test"


def logger():
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="PID=%(process)d LVL=%(levelname)s MSG=%(message)s",
        force=True,
    )

    return logging.getLogger()
