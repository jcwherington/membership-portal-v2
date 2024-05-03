import json
import sys
import logging
import os

import boto3
from botocore.exceptions import ClientError


def region():
    return 'ap-southeast-2'

def db_endpoint():
    return 'hyp-db.czwedxheq8hd.ap-southeast-2.rds.amazonaws.com'

def db_port():
    return '5432'

def db_name():
    return 'hyp-db'

def branch():
    return os.getenv('BRANCH')

def schema():
    return 'prod' if branch() == 'main' else 'test'

def get_db_credentials():
    SECRET_NAME = 'rds!db-570bc63b-c275-489b-b7b0-7dd4c321f3af'

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

def logger():
    logging.basicConfig(
        stream=sys.stdout, 
        level=logging.INFO, 
        format='PID=%(process)d LVL=%(levelname)s MSG=%(message)s', 
        force=True
    )
    return logging.getLogger()
