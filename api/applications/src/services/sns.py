import boto3
from botocore.exceptions import ClientError

from config import region, sns_topic_arn, logger
from common.error import SnsError


class Sns():

    def __init__(self):
        self.client = boto3.client('sns', region_name=region())
        self.logger = logger()
    
    def notify_outcome(self, message_attributes):
        self.logger.info(f'Publishing to sns topic: {message_attributes}')
        
        try:
            self.client.publish(
                TopicArn=sns_topic_arn(),
                Message='REJECTED',
                MessageAttributes=message_attributes
            )
        except ClientError as error:
            raise SnsError(error.response['Error']['Message'])
