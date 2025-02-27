# frozen_string_literal: true

require 'uri'
require_relative 'error'
require_relative 'constants'

def validate_event(event:)
  raise ValidationError, 'invalid event object' unless event.key?('Records')
  unless event['Records'][0]['EventSource'] == Constants::EVENT_SOURCE
    raise ValidationError, "invalid event source: #{event['Records'][0]['EventSource']}"
  end
  unless Constants::OUTCOME.include?(event['Records'][0]['Sns']['Message'])
    raise ValidationError, "'Outcome' is invalid: #{event['Records'][0]['Sns']['Message']}"
  end
  return if event['Records'][0]['Sns'].key?('MessageAttributes')

  raise ValidationError, "event object missing 'MessageAttributes' key"
end

def validate_message_attributes(message_attributes:)
  unless message_attributes.key?('Recipient')
    raise ValidationError, "'MessageAttributes' object missing 'Recipient' key"
  end
  raise ValidationError, "'MessageAttributes' object missing 'Name' key" unless message_attributes.key?('Name')
  return if URI::MailTo::EMAIL_REGEXP.match?(message_attributes['Recipient']['Value'])

  raise ValidationError, "'Recipient' is invalid: #{message_attributes['Recipient']['Value']}"
end
