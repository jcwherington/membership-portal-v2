import re
from datetime import datetime

from common.error import ValidationError

HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

def validate_event(event):
    if event['httpMethod'] not in HTTP_METHODS:
        raise ValidationError('invalid HTTP method')
    
    try:
        if event['httpMethod'] == 'GET':
            validate_get(event)
            return

        elif event['httpMethod'] == 'POST':
            validate_post(event)
            return

        elif event['httpMethod'] == 'PUT':
            validate_put(event)
            return

        elif event['httpMethod'] == 'DELETE':
            validate_delete(event)
            return
    
    except (KeyError, ValueError, TypeError):
        raise ValidationError('invalid event object')

def validate_get(event):
    if event['pathParameters']:
        try:
            int(event['pathParameters']['id'])
        except (KeyError, ValueError, TypeError):
            raise ValidationError('invalid id')
        
def validate_post(event):
    errors = validate_body(event['body'])

    if len(errors) > 0:
        raise ValidationError(f'the following parameters are invalid: {errors}')

def validate_put(event):
    if not event['pathParameters']:
        raise ValidationError('request missing path parameter')
    
    try:
        int(event['pathParameters']['id'])
    except (KeyError, ValueError, TypeError):
        raise ValidationError('invalid id')
    
    errors = validate_body(event['body'])

    if len(errors) > 0:
        raise ValidationError(f'the following parameters are invalid: {errors}')

def validate_delete(event):
    if not event['pathParameters']:
        raise ValidationError('request missing path parameter')
    
    try:
        int(event['pathParameters']['id'])
    except (KeyError, ValueError, TypeError):
        raise ValidationError('invalid id')

def validate_body(body):
    invalid_params = []

    if not re.match(r"^\S+@\S+\.\S+$", body['email']):
        invalid_params.append('email')
    
    try:
        if body['postCode']:
            int(body['postCode'])
            if not len(body['postCode']) == 4:
                invalid_params.append('post code')
    except (ValueError, TypeError):
        invalid_params.append('post code')
    
    try:
        if body['mobile']:
            int(body['mobile'])
            if not len(body['mobile']) == 10:
                invalid_params.append('mobile')
    except (ValueError, TypeError):
        invalid_params.append('mobile')
    
    try:
        if body['dob']:
            datetime.strptime(body['dob'], '%Y-%m-%d')
    except (ValueError, TypeError):
        invalid_params.append('dob')
    
    if not body['firstName']:
        invalid_params.append('first name')
    
    if not body['lastName']:
        invalid_params.append('last name')
    
    return invalid_params
