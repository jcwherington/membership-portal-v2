import boto3
from botocore.exceptions import ClientError
from botocore.client import BaseClient
from typing import Dict

from config import region, sns_topic_arn, logger
from common.error import SnsError


class Sns:

    def __init__(self) -> None:
        self.client: BaseClient = boto3.client("sns", region_name=region())
        self.logger = logger()

    def notify_outcome(self, message_attributes: Dict) -> None:
        self.logger.info(f"Publishing to sns topic: {message_attributes}")

        try:
            self.client.publish(
                TopicArn=sns_topic_arn(),
                Message="ACCEPTED",
                MessageAttributes=message_attributes,
            )
        except ClientError as error:
            raise SnsError(error.response["Error"]["Message"])
