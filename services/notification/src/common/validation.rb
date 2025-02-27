# frozen_string_literal: true

require 'uri'
require_relative 'error'
require_relative 'constants'

def validate_event(event:)
	raise ValidationError.new("invalid event object") unless event.key?("Records")
	raise ValidationError.new("invalid event source: #{event["Records"][0]["EventSource"]}") unless event["Records"][0]["EventSource"] == Constants::EVENT_SOURCE
	raise ValidationError.new("'Outcome' is invalid: #{event["Records"][0]["Sns"]["Message"]}") unless Constants::OUTCOME.include?(event["Records"][0]["Sns"]["Message"])
	raise ValidationError.new("event object missing 'MessageAttributes' key") unless event["Records"][0]["Sns"].key?("MessageAttributes")
end

def validate_message_attributes(message_attributes:)
	raise ValidationError.new("'MessageAttributes' object missing 'Recipient' key") unless message_attributes.key?('Recipient')
	raise ValidationError.new("'MessageAttributes' object missing 'Name' key") unless message_attributes.key?('Name')
	raise ValidationError.new("'Recipient' is invalid: #{message_attributes['Recipient']['Value']}") unless URI::MailTo::EMAIL_REGEXP.match?(message_attributes['Recipient']['Value'])
end
