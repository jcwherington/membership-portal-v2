require_relative 'services/ses'
require_relative 'services/s3'
# require_relative 'common/validation'
require_relative 'config'
require 'liquid'

def handler(event:, context:)

    logger = logger()
    logger.info(event)

    # validate_event(event)

    message_attributes = event['Records'][0]['Sns']['MessageAttributes']

    recipient = message_attributes['Recipient']['Value']
    template_variables = {
        'name' => message_attributes['Name']['Value'],
        'outcome' => message_attributes['Outcome']['Value']
    }

    s3 = S3.new
    template_data = s3.get_template()

    liquid_template = Liquid::Template.parse(template_data)
    html_data = liquid_template.render(template_variables)

    ses = Ses.new
    ses.send_email(recipient:, html_data:)

    { statusCode: 200, body: 'Email sent' }
end
