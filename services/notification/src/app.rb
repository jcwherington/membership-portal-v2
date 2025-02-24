require 'liquid'
require_relative 'services/ses'
require_relative 'services/s3'
require_relative 'common/validation'
require_relative 'common/error'
require_relative 'config'

def handler(event:, context:)

    logger = logger()
    logger.info(event)

    message_attributes = {}

    begin
        validate_event(event:)
        message_attributes = event['Records'][0]['Sns']['MessageAttributes']
        validate_message_attributes(message_attributes:)
    rescue ValidationError => error
        logger.error(error.inspect)
        return { statusCode: error.status, body: error.message }
    end

    recipient = message_attributes['Recipient']['Value']
    template_variables = {
        'name' => message_attributes['Name']['Value'],
        'outcome' => message_attributes['Outcome']['Value']
    }

    begin
        s3 = S3.new
        template_data = s3.get_template()

        liquid_template = Liquid::Template.parse(template_data)
        html_data = liquid_template.render(template_variables)
    
        ses = Ses.new
        ses.send_email(recipient:, html_data:)
    rescue ServiceError => error
        logger.error(error.message)
        return { statusCode: error.status, body: error.message }
    end

    { statusCode: 200, body: 'Email sent' }
end
