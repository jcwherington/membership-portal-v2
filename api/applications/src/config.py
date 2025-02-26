import sys
import os
import logging


def branch():
    return os.getenv('BRANCH')

def region():
    return 'us-west-2'

def table_name():
    return f'applications-{branch()}'

def dynamo_endpoint():
    return os.getenv('DYNAMO_ENDPOINT')

def sns_topic_arn():
    return os.getenv('SNS_TOPIC_ARN')

def logger():
    logging.basicConfig(
        stream=sys.stdout, 
        level=logging.INFO, 
        format='PID=%(process)d LVL=%(levelname)s MSG=%(message)s', 
        force=True
    )
    return logging.getLogger()
