import sys
import logging
from logging import Logger
import os


def region() -> str:
    return "us-west-2"


def db_endpoint() -> str:
    return os.getenv("DB_ENDPOINT")


def db_port() -> str:
    return os.getenv("DB_PORT")


def db_name() -> str:
    return os.getenv("DB_NAME")


def db_user() -> str:
    return os.getenv("DB_USER")


def db_password() -> str:
    return os.getenv("DB_PASSWORD")


def branch() -> str:
    return os.getenv("BRANCH")


def sns_topic_arn() -> str:
    return os.getenv("SNS_TOPIC_ARN")


def schema() -> str:
    match branch():
        case "local":
            return "local"
        case "main":
            return "prod"
        case _:
            return "test"


def logger() -> Logger:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="PID=%(process)d LVL=%(levelname)s MSG=%(message)s",
        force=True,
    )

    return logging.getLogger()
