from common.error import ValidationError

HTTP_METHODS = ['GET', 'POST', 'DELETE']

def validate_event(event):
    if event['httpMethod'] not in HTTP_METHODS:
        raise ValidationError('Invalid HTTP method')
    
    try:
        if event['httpMethod'] == 'GET':
            return

        elif event['httpMethod'] == 'POST':
            validate_post(event)
            return

        elif event['httpMethod'] == 'DELETE':
            validate_delete(event)
            return
    
    except (KeyError, ValueError, TypeError):
        raise ValidationError('Invalid event object')

def validate_post(event):
    if not event['body']:
        raise ValidationError('Request is missing body')
    
    if not event['body']['id']:
        raise ValidationError('Invalid \'id\' in body')

def validate_delete(event):
    if not event['pathParameters']:
        raise ValidationError('Request URL is missing path parameter')
    
    if not event['pathParameters']['id']:
        raise ValidationError('Invalid \'id\' in path parameter')
