# frozen_string_literal: true

require 'liquid'
require_relative 'services/ses'
require_relative 'services/s3'
require_relative 'common/validation'
require_relative 'common/error'
require_relative 'model/response'
require_relative 'config'

def handler(event:, _context:)
  logger = logger()
  logger.info(event)

  message_attributes = {}

  begin
    validate_event(event:)
    message_attributes = event['Records'][0]['Sns']['MessageAttributes']
    validate_message_attributes(message_attributes:)
  rescue ValidationError => e
    logger.error(e.inspect)
    return Response.new(e.status, e.message).resolve
  end

  recipient = message_attributes['Recipient']['Value']
  template_variables = {
    'name' => message_attributes['Name']['Value'],
    'outcome' => event['Records'][0]['Sns']['Message']
  }

  begin
    s3 = S3.new
    template_data = s3.template

    liquid_template = Liquid::Template.parse(template_data)
    html_data = liquid_template.render(template_variables)

    ses = Ses.new
    ses.send_email(recipient:, html_data:)
  rescue ServiceError => e
    logger.error(e.message)
    return Response.new(e.status, e.message).resolve
  end

  Response.new(200, 'Email sent successfully').resolve
end
