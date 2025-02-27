import boto3
from botocore.exceptions import ClientError
from botocore.client import BaseClient
from typing import Dict, Any, Optional

from config import region, table_name, dynamo_endpoint, logger
from model.application import Application
from common.error import DynamoError


class Dynamo:

    def __init__(self) -> None:
        self.client: BaseClient = boto3.client(
            "dynamodb", endpoint_url=dynamo_endpoint(), region_name=region()
        )
        self.logger = logger()

    def put_item(self, applicant: Application) -> None:
        self.logger.info(f"Adding applicant: {applicant}")

        try:
            self.client.put_item(TableName=table_name(), Item=applicant.to_dynamo())
        except ClientError as error:
            raise DynamoError(error.response["Error"]["Message"])

    def get_items(self) -> Dict[str, Any]:
        self.logger.info("Fetching all applicants")

        try:
            return self.client.scan(TableName=table_name())
        except ClientError as error:
            raise DynamoError(error.response["Error"]["Message"])

    def delete_item(self, id: int) -> Optional[Dict[str, Any]]:
        self.logger.info(f"Deleting applicant id: {id}")

        try:
            return self.client.delete_item(
                TableName=table_name(), Key={"id": {"S": id}}, ReturnValues="ALL_OLD"
            )
        except ClientError as error:
            raise DynamoError(error.response["Error"]["Message"])
