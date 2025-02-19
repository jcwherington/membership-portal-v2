from common.error import ValidationError

HTTP_METHODS = ['GET', 'POST', 'DELETE']

def validate_event(event):   
    match event['httpMethod']:
        case 'GET':
            return
        case 'POST':
            validate_post(event)
            return
        case 'DELETE':
            validate_delete(event)
            return
        case _:
            raise ValidationError('Invalid HTTP method')

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
