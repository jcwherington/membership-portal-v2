import json
import sys
import logging
import os

import boto3
from botocore.exceptions import ClientError


def region():
    return 'us-west-2'

def db_endpoint():
    return os.getenv('DB_ENDPOINT')

def db_port():
    return os.getenv('DB_PORT')

def db_name():
    return os.getenv('DB_NAME')

def branch():
    return os.getenv('BRANCH')

def schema():
    match branch():
        case 'local':
            return 'local'
        case 'main':
            return 'prod'
        case _:
            return 'test'

def get_db_credentials():
    if branch() == 'local':
        return local_db_credentials()
    
    SECRET_NAME = '<secret_name>'

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region()
    )

    try:
        response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
    except ClientError as error:
        logging.error(error)
        raise error

    return json.loads(response['SecretString'])

def local_db_credentials():
    return {
        'username': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }

def logger():
    logging.basicConfig(
        stream=sys.stdout, 
        level=logging.INFO, 
        format='PID=%(process)d LVL=%(levelname)s MSG=%(message)s', 
        force=True
    )
    return logging.getLogger()
