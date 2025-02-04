import boto3
from botocore.exceptions import ClientError

from config import region, table_name, dynamo_endpoint
from model.application import Application
from common.error import DynamoError


class Dynamo():

    def __init__(self):
        self.client = boto3.client('dynamodb', endpoint_url=dynamo_endpoint(), region_name=region())
    
    def put_item(self, applicant: Application):
        try:
            self.client.put_item(
                TableName=table_name(),
                Item=applicant.to_dynamo()
            )
        except ClientError as error:
            raise DynamoError(error.response['Error']['Message'])
    
    def get_items(self):
        try:
            return self.client.scan(
                TableName=table_name()
            )
        except ClientError as error:
            raise DynamoError(error.response['Error']['Message'])
    
    def delete_item(self, id: int):
        try:
            self.client.delete_item(
                TableName=table_name(),
                Key={
                    'id': {
                        'S': id
                    }
                },
                ReturnValues='ALL_OLD'
            )
        except ClientError as error:
            raise DynamoError(error.response['Error']['Message'])
