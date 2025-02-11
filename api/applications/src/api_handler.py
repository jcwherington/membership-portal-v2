from model.application import Application
from services.dynamo import Dynamo
from common.error import ValidationError


def handle_event(event):      
    dynamo = Dynamo()

    if event['httpMethod'] == 'GET':
        return handle_get(dynamo)

    elif event['httpMethod'] == 'POST':  
        handle_post(event, dynamo)
        return

    elif event['httpMethod'] == 'DELETE':
        handle_delete(event, dynamo)
        return

    else:
        raise ValidationError('Invalid HTTP method')
    
def handle_get(dynamo):
    result = dynamo.get_items()

    data = []
    if result['Items']:
        for applicant_data in result['Items']:
            applicant = Application.from_dynamo(applicant_data)
            data.append(applicant)

    return data

def handle_post(event, dynamo):
    applicant = Application.from_event(event)
    dynamo.put_item(applicant)

def handle_delete(event, dynamo):
    dynamo.delete_item(event['pathParameters']['id'])
