import sys
import os
import logging
from logging import Logger


def branch() -> str:
    return os.getenv("BRANCH")


def region() -> str:
    return "us-west-2"


def table_name() -> str:
    return f"applications-{branch()}"


def dynamo_endpoint() -> str:
    return os.getenv("DYNAMO_ENDPOINT")


def sns_topic_arn() -> str:
    return os.getenv("SNS_TOPIC_ARN")


def logger() -> Logger:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="PID=%(process)d LVL=%(levelname)s MSG=%(message)s",
        force=True,
    )
    return logging.getLogger()
